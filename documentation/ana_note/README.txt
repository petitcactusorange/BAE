! $Id: README.txt 5804 2011-06-08 09:27:16Z tskwarni $
!-----------------------------------------------------------------------------
! Project: LHCb-latex-template
! Purpose: to be used as template for directory structure for LHCb note or paper
! Responsible: Tomasz Skwarnicki
! Editing policy: contact the responsible person before commiting any changes  
!-----------------------------------------------------------------------------

Basic usage:

1. How to use as starting template for projects within lhcbdocs repository:
   
   Do this only once (this assumes your project directory does not exist yet):

     svn cp svn+ssh://svn.cern.ch/reps/lhcbdocs/Templates/LHCb-latex-template \
            svn+ssh://svn.cern.ch/reps/lhcbdocs/Users/your_user_id/your_document_project_name \
            -m"copied LHCb-latex-template template for Users/your_user_id/your_document_project_name"
     svn co svn+ssh://svn.cern.ch/reps/lhcbdocs/Users/your_user_id/your_document_project_name
        edit your_document_project_name/README.txt
     svn ci -m"customized README file"  
     rm -rf your_document_project_name

   If you previously created the project directory it is best to delete it and follow the instructions above
   or alternatively you can copy conents of LHCb-latex-template one-by-one (i.e. "latest", "drafts" etc.) 
   into your destination. 

   Then whenever you want to modify your project:

     svn co svn+ssh://svn.cern.ch/reps/lhcbdocs/Users/your_user_id/your_document_project_name/latest

   change content of latest/ and commit back to repository (see SVN docs).

2. Explanation of the development directory structure 

   latest/ is a so called "trunk" of your project. This is where you develop it. 

   latest/latex/ - for all TeX source files; also working directory for making output file
                   (see example *.tex files in this template)

   latest/latex/Makefile - example file how to make output file using "make" utility:
                   edit for your project - supply list of all your source files  
                   then "make all" to produce output
                   "make clean" to delete temporary files (output is not removed)

   latest/latex/figs/ - put all your figures here (just a recommendation)

   latest/doc/release.notes - use to document purpose of the document and changes you make to your project (recommendation)

3. How to use as starting template for projects outside lhcbdocs repository - projects maintained in plain file system:

  In directory in which you want to create a project:

     svn export svn+ssh://svn.cern.ch/reps/lhcbdocs/Templates/LHCb-latex-template your_project_directory_name
      
  or just latest/ part:

   svn export svn+ssh://svn.cern.ch/reps/lhcbdocs/Templates/LHCb-latex-template/latest your_project_directory_name


4. How to use as starting template for projects in other (e.g. private) repository 

  In temporary directory:

     svn export svn+ssh://svn.cern.ch/reps/lhcbdocs/Templates/LHCb-latex-template your_document_project_name
     cd your_document_project_name
       (edit README.txt; edit other files; clean-up)
     svn import svn+ssh://svn.cern.ch/reps/your_private_repository/rest_of_the_path_in_repository \
           -m"first import of my document project"

5. Explanation of the drafts/ directory for tagged versions:

  The main directory contains two directories:

   latest/    - latest version of the project (so called "trunk" directory)
                Check this directory out of repository, modify, commit the changes.

   drafts/    - snapshots (named releases) of the project (so called "tags" directory)

   To tag:

     svn cp svn+ssh://svn.cern.ch/reps/lhcbdocs/Users/your_user_id/your_document_project_name/latest \
            svn+ssh://svn.cern.ch/reps/lhcbdocs/Users/your_user_id/your_document_project_name/drafts/v2r0 \
            -m"created version v2r0"

      You should never try to change the tagged copies (do not use "svn commit" in the drafts/ area).

      Do not tag every revision (you can get to them in svn via revision number!). 
      Tag only special revisions (e.g. posted versions).
      Edit latest/docs/release.notes and insert comment about the tag e.g. add
          !================== v2r0 =============
          ! YYY-MM-DD your_name - version posted to referees





  