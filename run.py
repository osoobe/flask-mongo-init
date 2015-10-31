#!/usr/bin/env python
# coding: utf-8

import argparse
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
import os
import sys

MAIN_FOLDER = os.path.abspath(os.path.dirname(__file__))
CSS_FOLDER = os.path.join(MAIN_FOLDER, 'static', "src", "css")
MAIN_LESS_FILE = os.path.join(MAIN_FOLDER, 'static', "src", "less", "style.less")
COMPILE_CSS_FILE = os.path.join(MAIN_FOLDER, "static", "dst", "css", "style.min.css")

###############################################################################
# Options
###############################################################################
PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    '-m', '--minify', dest='minify', action='store_true',
    help='compiles files into minified version before deploying')
PARSER.add_argument(
    '-s', '--start', dest='start', action='store_true',
    help='starts the app with storage_path pointing to temp')
PARSER.add_argument(
    '-d', '--debug', dest='debug', action='store_true',
    help='starts the app in debugging mode with storage_path pointing to temp')
PARSER.add_argument(
    '-c', '--clean', dest='clean', action='store_true',
    help='remove all bytecodes, i.e. *.pyc')
PARSER.add_argument(
    '-w', '--watch', dest='watch', action='store_true',
    help='recompile less files upon change')
ARGS = PARSER.parse_args()

###############################################################################
# Setup virtual envirnoment
###############################################################################

activate_this = "temp/bin/activate_this.py"
if not os.path.exists(activate_this):
  if os.path.exists("temp/Scripts/activate_this.py"):
    activate_this = "temp/Scripts/activate_this.py"

if not hasattr(sys, 'real_prefix'):
    execfile(activate_this, dict(__file__=activate_this))

###############################################################################
# Helpers
###############################################################################
def print_out(script, filename=''):
  timestamp = datetime.now().strftime('%H:%M:%S')
  if not filename:
    filename = '-' * 46
    script = script.rjust(12, '-')
  print '[%s] %12s %s' % (timestamp, script, filename)


def make_dirs(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)

def make_file_dirs(file_path):
  file_dir = os.path.dirname(file_path)
  if not os.path.isdir(file_dir):
    make_dirs(file_dir)

def remove_file_dir(file_dir):
  if os.path.exists(file_dir):
    if os.path.isdir(file_dir):
      shutil.rmtree(file_dir)
    else:
      os.remove(file_dir)


def clean_files():
  bad_endings = ['pyc', 'pyo', '~']
  print_out(
      'CLEAN FILES',
      'Removing files: %s' % ', '.join(['*%s' % e for e in bad_endings]), )
  for root, _, files in os.walk('.'):
    for filename in files:
      for bad_ending in bad_endings:
        if filename.endswith(bad_ending):
          remove_file_dir(os.path.join(root, filename))


def merge_files(source, target):
  fout = open(target, 'a')
  for line in open(source):
    fout.write(line)
  fout.close()


def os_execute(executable, args, source, target, append=False):
  operator = '>>' if append else '>'
  os.system('"%s" %s %s %s %s' % (executable, args, source, operator, target))


def is_dirty(source, target):
  if not os.access(target, os.O_RDONLY):
    return True
  return os.stat(source).st_mtime - os.stat(target).st_mtime > 0


def is_style_modified(target):
  less_dir = os.path.dirname(MAIN_LESS_FILE)
  if os.path.exists(target):
    return True
  for root, _, files in os.walk(less_dir):
    for filename in files:
      path = os.path.join(root, filename)
      print_out('CHANGED DETECTED', path)
      if path.endswith('.less') and is_dirty(path, target):
        return True
  return False

########################################################################
# Guards
########################################################################
GUARD_FOLDER = os.path.join(MAIN_FOLDER, "temp", "guards")
COMPILE_CSS_GUARD = os.path.join(GUARD_FOLDER, "less.guard")


def make_temp():
  if not os.path.exists(GUARD_FOLDER):
    make_dirs(GUARD_FOLDER)


def guard_is_newer(guard, watched):
  if os.path.exists(guard):
    return os.path.getmtime(guard) > os.path.getmtime(watched)
  return False


def make_guard(fname, cmd, spec):
  make_temp()
  with open(fname, 'w') as guard:
    guard.write('Prevents %s execution if newer than %s' % (cmd, spec))


########################################################################
# App Environment
########################################################################
def compile_styles():
  print_out('COMPILING', 'less files')
  make_file_dirs(COMPILE_CSS_FILE)
  os.system('lessc %s %s' % (MAIN_LESS_FILE, COMPILE_CSS_FILE))
  spec = os.stat(COMPILE_CSS_FILE).st_mtime
  make_guard(COMPILE_CSS_GUARD, "lessc", spec)
  print_out('DONE', 'compiling less files')


def run_watch_styles():
  print_out('DONE', 'and watching for changes (Ctrl+C to stop)')
  while True:
    time.sleep(0.5)
    if is_style_modified(COMPILE_CSS_GUARD):
      compile_styles()


def run_app():
  from application import app
  import flask_config
  assert flask_config

  app.run(host="0.0.0.0", port=9091)


def debug_app():
  from application import app
  import flask_config
  assert flask_config

  app.run(host="0.0.0.0", port=9091, debug=True)


def run():
  if len(sys.argv) == 1:
    PARSER.print_help()
    sys.exit(1)

  if ARGS.minify:
    compile_styles()

  if ARGS.watch:
    run_watch_styles()

  if ARGS.clean:
    clean_files()

  if ARGS.start:
    run_app()

  if ARGS.debug:
    debug_app()


if __name__ == '__main__':
  run()
