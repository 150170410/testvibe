
import argparse
import importlib
import os
import sys
import re

import tqdm

import testvibe

try:
    import settings
except ImportError:
    # NOTE(niklas9):
    # * this should only happen during testing, otherwise a global settings
    #   be importable for every project
    settings = None


class CLIHandler(object):

    DEFAULT_INSTALL_DIR = 'default_install/'
    FILENAME_SETTINGS = 'settings.py'
    FILENAME_RUNLIST = 'RUNLIST'
    FILENAME_TESTSUITE = 'example_testsuite.py'
    INIT_FILENAME = '__init__.py'
    FILEMODE_READ = 'r'
    FILEMODE_WRITE = 'w'
    RUNLIST_COMMENT_PREFIX = '#'
    PLACEHOLDER_NAME = '<Example>'
    RE_VALID_NAME = r'^[A-Za-z0-9_]+$'
    CMD_STARTPROJECT = 'startproject'
    CMD_ADDTESTGROUP = 'addtestgroup'
    CMD_RUN = 'run'
    CMDS_WITH_NAME_ARG = (CMD_STARTPROJECT, CMD_ADDTESTGROUP)
    DEFAULT_LOG_DIR = '%s/logs'
    CURRENT_WORKING_DIR = '.'  # no windoze support :)

    args = None
    verbosity = None

    def __init__(self, args):
        self.args = args
        log_level = testvibe.logger.LOG_LEVEL_DEBUG
        if settings is not None and not settings.LOG_LEVEL_DEBUG:
            log_level = testvibe.logger.LOG_LEVEL_PROD
        self.verbosity = False
        if 'verbosity' in self.args and self.args.verbosity:
            self.verbosity = True
        self.log = testvibe.logger.Log(log_level=log_level,
                                       use_stdout=self.verbosity)

    def execute(self):
        cmd = self.args.cmd
        if cmd in self.CMDS_WITH_NAME_ARG:
            name = self.args.name
            if not self._is_valid_name(name):
                # NOTE(niklas9):
                # * for example dashes (-) in names will cause unimportable
                #   projects in Python
                sys.stderr.write('error: unsupported characters in name\n')
                sys.exit(1)
            if cmd == self.CMD_STARTPROJECT:
                self.cmd_startproject(self.args.name)
            elif cmd == self.CMD_ADDTESTGROUP:
                self.cmd_addtestgroup(self.args.name)
        elif cmd == self.CMD_RUN:
            self.cmd_run()

    def cmd_run(self):
        runlists = self._get_runlists()
        if len(runlists) == 0:
            sys.stderr.write('no runlists found...\n')
            sys.exit(1)
        for rl in runlists:
            if '/' in rl:
                tgroup = rl.split('/')[0]
                tsuites = self._parse_runlist(rl)
                self.log.info('starting test run on testgroup <%s>' % tgroup)
                self._run_tsuites(tgroup, tsuites)
            else:
                tgroup = os.getcwd().split('/')[-1]
                tsuites = self._parse_runlist(rl)
                self.log.info('starting test run on all testsuites in current dir')
                self._run_tsuites(tgroup, tsuites)

    def _run_tsuites(self, tgroup, tsuites):
        self.log.debug('found %d test suites' % len(tsuites))
        len_tsuites = len(tsuites)
        if self.verbosity:
            iterable = xrange(len_tsuites)
        else:
            iterable = tqdm.tqdm(range(len_tsuites), leave=True, desc=tgroup)
        for i in iterable:
            tsuite = tsuites[i]
            if '/' in tsuite:
                tsuite = tsuite.split('/')[-1]
            self.log.debug('initating run on testsuite <%s>' % tsuite)
            # TODO(niklas9):
            # * add exception handling for the importing below.. the user can
            #   enter lots of bad stuff in the runlists.. we should give them a
            #   hint
            ts = importlib.import_module('.%s' % tsuite[:-3],
                                         package=tgroup)
            tsuite_classes = self._get_all_tsuite_classes(ts)
            if len(tsuite_classes) == 0:
                # TODO(niklas9):
                # * this is actually too late.. should do some sanity check on
                #   all runlists before initiating a test run..
                #   like "validating runlists".. could be a separate cmd to
                #   tvctl as well
                sys.stderr.write('no subclasses of testvibe.Testsuite found\n')
                sys.exit(1)
            for tsuite_class in tsuite_classes:
                tcs = self._get_all_tcases(tsuite_class)
                tsuite_class_i = tsuite_class()
                for tc in tcs:
                    # TODO(niklas9):
                    # * I don't get why class instance is second arg below.. should
                    #   replace 'self' so should be the first one?!!
                    tsuite_class_i.test(tc, tsuite_class_i)

    def cmd_startproject(self, name):
        self._exit_if_dir_exists(name)
        os.makedirs(self.DEFAULT_LOG_DIR % name)
        self._copy_file(name, CLIHandler.FILENAME_SETTINGS,
                       search=CLIHandler.PLACEHOLDER_NAME, replace=name)
        self._add_init_file(name)

    def cmd_addtestgroup(self, name):
        self._exit_if_dir_exists(name)
        os.makedirs(name)
        self._add_init_file(name)
        self._copy_file(name, self.FILENAME_RUNLIST)
        self._copy_file(name, self.FILENAME_TESTSUITE)

    @staticmethod
    def _add_init_file(path):
        p = '%s/%s' % (path, CLIHandler.INIT_FILENAME)
        with open(p, CLIHandler.FILEMODE_WRITE) as f:
            pass  # just an empty file

    @staticmethod
    def _copy_file(dir_name, filename, search=None, replace=None):
        with open(CLIHandler._get_src(filename), CLIHandler.FILEMODE_READ) as f:
            src_content = f.read()
        if search is not None and replace is not None:
            src_content = src_content.replace(search, replace)
        with open('%s/%s' % (dir_name, filename), CLIHandler.FILEMODE_WRITE) as f:
            f.write(src_content)

    @staticmethod
    def _get_src(filename):
        return ('%s/%s%s' % (os.path.dirname(testvibe.__file__),
                             CLIHandler.DEFAULT_INSTALL_DIR, filename))

    @staticmethod
    def _exit_if_dir_exists(dir_name):
         if os.path.exists(dir_name):
            sys.stderr.write('command error: \'%s\' already exists\n'
                             % os.path.abspath(dir_name))
            sys.exit(1)

    @staticmethod
    def _is_valid_name(s):
        return re.match(CLIHandler.RE_VALID_NAME, s) is not None

    @staticmethod
    def _get_all_dirs(path):
        dirs = set()
        for f in os.listdir(path):
            if os.path.isdir(f):
                dirs.add(f)
        return dirs

    @staticmethod
    def _get_runlists():
        runlists = set()
        if os.path.exists(CLIHandler.FILENAME_RUNLIST):
            runlists.add(CLIHandler.FILENAME_RUNLIST)
        else:
            dirs = CLIHandler._get_all_dirs(CLIHandler.CURRENT_WORKING_DIR)
            for d in dirs:
                for f in os.listdir(d):
                    if f == CLIHandler.FILENAME_RUNLIST:
                        runlists.add('%s/%s' % (d, f))
        return runlists

    @staticmethod
    def _get_all_tcases(cl):
        tcases = set()
        reserved_names = testvibe.Testsuite.RESERVED_NAMES
        for o in dir(cl):
            if o.startswith('_'):  continue  # no private methods
            if o in reserved_names:  continue  # skip the reserved method names
            if o not in cl.__dict__:  continue  # don't consider inherited
            if not callable(getattr(cl, o)):  continue  # only methods
            tcases.add(getattr(cl, o))
        return tcases

    @staticmethod
    def _get_all_tsuite_classes(module):
        tsuites = set()
        for o in dir(module):
            co = getattr(module, o)  # co == call object
            if isinstance(co, type) and issubclass(co, testvibe.Testsuite):
                tsuites.add(co)
        return tsuites

    @staticmethod
    def _parse_runlist(path):
        tsuites = list()  # dups are fine, if one wants to rerun tsuites
        with open(path, CLIHandler.FILEMODE_READ) as f:
            content = f.read()
        for line in content.splitlines():
            if not line.startswith(CLIHandler.RUNLIST_COMMENT_PREFIX):
                tsuites.append(line)
        return tuple(tsuites)


class ArgumentParserWithError(argparse.ArgumentParser):

    def error(self, msg):
        sys.stderr.write('error: %s\n' % msg)
        self.print_help()
        sys.exit(1)
