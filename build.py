import os, sys
import shutil

def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

def main():

    script_dir = os.path.dirname(os.path.realpath(__file__))
    build_dir = os.path.join(script_dir, 'build')

    if sys.argv[1] == 'b':
        if os.path.isdir(build_dir):
            shutil.rmtree(build_dir)
        os.makedirs(build_dir)

        cdir = os.getcwd()
        copyDirectory(os.path.join(script_dir, 'chapters'), os.path.join(build_dir, 'chapters'))
        copyDirectory(os.path.join(script_dir, 'gfx'), os.path.join(build_dir, 'gfx'))
        shutil.copyfile('thesis.tex', os.path.join(build_dir, 'thesis.tex'))

        cdir = os.getcwd()
        os.chdir(build_dir)
        #os.system('arara thesis.tex')
        os.system('rubber --pdf thesis.tex')
        os.chdir(cdir)

    if sys.argv[1] == 'c':
        os.rmdir(build_dir)

if __name__=='__main__':
    main()


