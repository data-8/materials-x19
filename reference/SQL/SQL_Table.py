import numbers
import IPython
import sqlite3
from datascience import *
import numpy as np

class SQL_DB:
    """Provide Tables interface to SQL database."""
    def __init__(self, database_path):
        self.path = database_path
        self.conn = sqlite3.connect(self.path, 
                                    detect_types=sqlite3.PARSE_COLNAMES)
        self.status = "connected"

    def close(self):
        self.conn.close()
        self.status = "closed"
    
    @property
    def tables(self):
        names = self.conn.execute('select name from sqlite_master;').fetchall()
        return [name[0] for name in names]
    
class SQL_Table:
    def __init__(self, DB, tablename):
        """Initialize SQL_Table object with database and table name."""
        self.DB = DB
        self.tablename = tablename
    
    # Methods for manipulating the database around the table
    @property    
    def exists(self):
        """Return schema as SQL create statement, if table exists."""
        create = self.DB.conn.execute('select sql from sqlite_master where name=?;', 
                          (self.tablename,)).fetchall()
        return create[0][0] if create else False
    
    def _sqlexec(self, query, verbose=False):
        """Wrap verbose processing around SQL query."""
        if verbose:
            print(query)
        return self.DB.conn.execute(query)
    
    def table(self, verbose=False, limit=None):
        """Create a Table from table from a SQL database."""
        if limit is None:
            rows = self._sqlexec('SELECT * FROM %s;' % self.tablename, verbose).fetchall()
        else:
            rows = self._sqlexec('SELECT * FROM %s LIMIT %s;' % 
                                 (self.tablename, limit), verbose).fetchall()
        return Table(self.labels).with_rows(rows)
        
    def create(self, table, verbose=False):
        """Create SQL database table from a Table."""
        cols = _build_list(table.labels)
        self._sqlexec("CREATE TABLE %s %s;" % (self.tablename, cols), verbose)
        for row in table.rows:  
            self._sqlexec('INSERT INTO %s VALUES %s;' % (self.tablename, tuple(row)), verbose)
        self.DB.conn.commit()
        
    def remove(self, verbose=False):
        """Remove the underlying SQL table."""
        self._sqlexec('DROP TABLE %s;' % self.tablename, verbose)
    
    def rename(self, tablename, verbose=False):
        self._sqlexec('ALTER TABLE %s RENAME TO %s;' % (self.tablename, tablename), verbose)
        self.tablename = tablename
    
    def replicate(self, tablename, verbose=False):
        self._sqlexec('CREATE TABLE %s AS SELECT * FROM %s;' % 
                      (tablename, self.tablename), verbose)
        return SQL_Table(self.DB, tablename)

        
    # Table methods analogs for SQL_Tables
    
    @property
    def labels(self):
        """Return list of column names of a SQL table."""
        cursor = self.DB.conn.execute('SELECT * FROM %s LIMIT 1;' % self.tablename)
        col_names = [col[0] for col in cursor.description]
        return col_names
    
    @property
    def num_columns(self):
        """Number of columns."""
        return len(self.labels)
    
    @property
    def columns(self):
        return self.table().columns
    
    @property
    def num_rows(self):
        label = self.labels[0]
        return self.DB.conn.execute("SELECT count(%s) FROM %s;" %
                                    (label, self.tablename)).fetchall()[0][0]
    @property
    def rows(self):
        return self.table().rows
    
    def column(self, index_or_label, verbose=False):
        label = self._as_label(index_or_label)
        return np.array([row[0] for row in 
                         self._sqlexec('SELECT %s from %s;' % 
                                       (label, self.tablename), verbose).fetchall()])
    
    def select(self, label_or_labels, verbose=False):
        """Return a Table with selected column or columns by label."""
        
        if isinstance(label_or_labels, str):
            label_str = label_or_labels
            labels = [label_or_labels]
        else:
            label_str = _build_sequence(label_or_labels)
            labels = label_or_labels
        rows = self._sqlexec('SELECT %s from %s;' % 
                             (label_str, self.tablename), verbose).fetchall()
        return Table(labels).with_rows(rows)
    
    def where(self, label, value_or_predicate=None, other=None, verbose=False):
        if value_or_predicate is None:
            rows =  self._sqlexec('SELECT * FROM %s WHERE %s;' % 
                                  (self.tablename, label), verbose).fetchall()
        elif other is None:
            if isinstance(value_or_predicate, str):
                if value_or_predicate in self.labels:
                    compare = value_or_predicate
                else:
                    compare = '"%s"' % value_or_predicate
            else:
                compare = value_or_predicate
            rows =  self._sqlexec('SELECT * FROM %s WHERE %s = %s;' % 
                                  (self.tablename, label, compare), verbose).fetchall()
        else:
            rows =  self._sqlexec('SELECT * FROM %s WHERE %s %s %s;' % 
                                  (self.tablename, label, value_or_predicate, other), verbose).fetchall()
        return Table(self.labels).with_rows(rows)
    
    def join(self, column_label, other, other_label=None, verbose=False):
        if other_label is None:
            other_label = column_label
        if isinstance(other, SQL_Table):
            labels1 = [lbl for lbl in self.labels if lbl != column_label]
            labels2 = [lbl for lbl in other.labels if lbl != other_label]
            labels = [column_label] + labels1 + labels2
            
            rows = self._sqlexec('SELECT %s FROM %s,%s WHERE %s.%s = %s.%s;' %
                                 (_build_sequence(labels),
                                  self.tablename, other.tablename,
                                  self.tablename, column_label,
                                  other.tablename, other_label), verbose)
            return Table(labels).with_rows(rows)
        elif isinstance(other, Table):
            tbl = self.table()
            return tbl.join(column_label, other, other_label)
        else:
            raise "Other must be a table"
            
    def sort(self, column_or_label, descending=False, distinct=False, verbose=False):
        assert not distinct, "distinct not supported on SQL_Table.sort"
        assert isinstance(column_or_label, str), "Column numbers not supported on SQL_Table"
        odr = column_or_label if not descending else "-"+column_or_label
        rows = self._sqlexec('SELECT * from %s order by %s;' % 
                             (self.tablename, odr), verbose).fetchall()
        return Table(self.labels).with_rows(rows)
    
    def drop(self, column_label_or_labels):
        tbl = self.table()
        return tbl.drop(column_label_or_labels)
    
    def group(self, column_or_label, collect=None, verbose=None):
        assert isinstance(column_or_label, str), "Column numbers not supported on SQL_Table"
        if collect is None:
            rows = self._sqlexec('SELECT %s, count(%s) AS count FROM %s GROUP BY %s;' % 
                             (column_or_label, column_or_label,
                              self.tablename, column_or_label), verbose).fetchall()
            return Table([column_or_label, "count"]).with_rows(rows)
        else:
            tbl = self.table()
            return tbl.group(column_or_label, collect)
    
    @classmethod
    def read_table(cls, filepath_or_buffer, *args, **vargs):
        """Read a table from a file or web address.""" 
        return Table.read_table(filepath_or_buffer, *args, **vargs)
    
    @classmethod
    def from_df(cls, df):
        """Convert a Pandas DataFrame into a Table."""
        return Table.from_df(df)

    @classmethod
    def from_array(cls, arr):
        """Convert a structured NumPy array into a Table."""
        return Table.from_array(arr)
    
    ##########################                                                  
    # Exporting / Displaying #                                                  
    ##########################    
    
    def _repr_html_(self):
        return self.as_html()
    
    max_str_rows = 10
    
    def __str__(self):
        head = "SQL_TABLE %s of %s\n" % (self.tablename, self.DB.path)
        return head + self.as_text(self.max_str_rows)

    __repr__ = __str__
    
    def show(self, max_rows=0, verbose=False):
        """Display the table."""
        IPython.display.display(IPython.display.HTML(self.as_html(max_rows, verbose=verbose)))

    def as_text(self, max_rows=0, sep=" | ", verbose=False):
        if max_rows:
            tbl = self.table(verbose=verbose, limit=max_rows)
        else:
            tbl = self.table(verbose=verbose)
        return tbl.as_text(max_rows, sep)
    
    def as_html(self, max_rows=0, verbose=False):
        if max_rows:
            tbl = self.table(verbose=verbose, limit=max_rows)
        else:
            tbl = self.table(verbose=verbose)
        return "SQL Table %s<p>" % self.tablename + tbl.as_html(max_rows)        
    
    #################                                                           
    # Magic Methods #                                                           
    #################                                                           

    def __getitem__(self, index_or_label):
        label = self._as_label(index_or_label)
        return self.column(label)

    def __setitem__(self, label, values):
        self.append_column(label, values)

    def __iter__(self):
        return iter(self.labels)

    
    def __len__(self):
        return len(self.labels)
    
    def __delitem__(self, label):
        raise "Unsupported"
    
    ############                                                                
    # Mutation #                                                                
    ############                                                                

    def set_format(self, column_label_or_labels, formatter):
        raise "Unsupported"
        
    def move_to_start(self, column_label):
        raise "Unsupported"
    
    def move_to_end(self, column_label):
        raise "Unsupported"
    
    def append(self, row_or_table, verbose=False):
        """Append a row or all rows of a table. An appended table must have all
        columns of self."""
        if not row_or_table:
            return
        if isinstance(row_or_table, Table):
            for row in row_or_table.rows:
                self._sqlexec('INSERT INTO %s VALUES %s;' % 
                              (self.tablename, 
                               str(tuple(row))), verbose)
        else:
            row = str(tuple(row_or_table))
            self._sqlexec('INSERT INTO %s VALUES %s;' % 
                          (self.tablename, row), verbose)
        self.DB.conn.commit()
        
    def append_column(self, label, values, verbose=False):
        """Appends a column to the table or replaces a column."""
        raise "SQL_Table unsupported"

    def _as_label(self, index_or_label):
        """Convert index to label."""
        if isinstance(index_or_label, str):
            return index_or_label
        if isinstance(index_or_label, numbers.Integral):
            return self.labels[index_or_label]
        else:
            raise ValueError(str(index_or_label) + ' is not a label or index')

    def _as_labels(self, label_or_labels):
        """Convert single label to list and convert indices to labels."""
        return [self._as_label(s) for s in _as_labels(label_or_labels)]

    def _unused_label(self, label):
        """Generate an unused label."""
        original = label
        existing = self.labels
        i = 2
        while label in existing:
            label = '{}_{}'.format(original, i)
            i += 1
        return label
    
    # For all remaining Table methods, create a Table and invoke method
    def __getattr__(self, name):
        def handlerFunction(*args,**kwargs):
            if kwargs:
                return getattr(self.table(),name)(*args, **kwargs)
            else:
                return getattr(self.table(),name)(*args)
        return handlerFunction

def _build_list(s):
    """Return string representing column name tuple."""
    res = "("
    for v in s[:-1]:
        res = res + v + ", "
    res = res + s[-1] + ")"
    return res

def _build_sequence(s):
    """Return string representing column name tuple."""
    res = ""
    for v in s[:-1]:
        res = res + v + ", "
    res = res + s[-1]
    return res

# __get_attr__ seems to prevent Jupyter from finding _repr_html, so force it
get_ipython().display_formatter.formatters['text/html'].for_type(SQL_Table, SQL_Table._repr_html_)