# R-Module
Introductory materials for data analysis in R.

# Steps to run R in Jupyter notebook

1. Ensure proper installation of R (https://www.r-project.org/)
2. Ensure proper installation of Python and Conda
3. Start an R terminal by opening up Terminal on Mac and typing `R`
4. Enter the command `install.packages(c('repr', 'IRdisplay', 'evaluate', 'crayon', 'pbdZMQ', 'devtools', 'uuid', 'digest'))`
5. Then, enter `devtools::install_github('IRkernel/IRkernel')`
6. Finally, enter `IRkernel::installspec()`

Now, exit the R terminal using `quit()`. Open up the Jupyter interface using `jupyter notebook`. Now you will notice that there are two options for picking kernels: Python 3 and R. Select R to run R code in Jupyter notebooks. The extension of the notebook remains to be .ipynb and not .rmd
