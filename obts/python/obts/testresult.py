

'''
Unit Test Result
Represent a single test (usually a single binary execution or file tested)
All parameters can be ommmited

- name: Verbose formated test name. Default is 'test'
- label: simple ascii-str test identifier, without spaces. 
  Can use '.' to create any possible hierarchy of tests in the TestSuite.
  Default is sane as name
- desc: Long description of the test. Default is ''
- cmd: Command executed to run the test, or anything explaining how the test is run.
  Default is ''
- valid: Did the test suceeded. Default is false
- status: Some program may have a status (prog ret value, err code, short status str).
  Can be used to identify the error. Default is '0'
- output: Contains the complete output of the test (valid or not). Default is ''
- expected: Contains the complete expected output (for diff tests).
  Usually given only when test failed. Default is ''
- err_short: Short description of the error, Usually 1/2 lines. Default is ''
- err_long: Precise description of the error, many lines. Default is ''
- err_full: Use for really long generated error messages / files. Default is ''
- custom: dict<string, string>, to store extra informations. Default is {}

- id: Used for tests ordering, only for displaying results. Nothing to do with run order.



'''
class UTResult:

    def __init__(self, name='test',
                 label=None,
                 desc='',
                 cmd='',
                 valid=False,
                 status=0,
                 output='',
                 expected='',
                 err_short='',
                 err_long='',
                 err_full='',
                 custom=dict()):
        if label is None:
            label = name

        self.name = name
        self.label = label
        self.desc = desc
        self.cmd = cmd
        self.valid = bool(valid)
        self.status = str(status)
        self.output = output
        self.expected = expected
        self.err_short = err_short
        self.err_long = err_long
        self.err_full = err_full
        self.custom = custom

        self.id = None



'''
Test Suite Result
A Test Suite result is an ordered sequence of unit tests. 
One binary execution run multiple tests (unit test), and generate one testsuite result.
There may be multiple test suites for one project

- proj_name: name of the current project. Can use '.' to divide into subprojects. 
  Only required field
- proj_tag: Tag to identify wich project part being worked on. Usually the git branch name. 
  Default is 'master'
- proj_ver: Version of the projet. Default is '1.0.0'
proj_id: If versioning used, can be the commit hash for example. Default is ''
- label: TestSuite unique label for the projet. Use '.' to divide testsuite by groups. 
  Default is the project_name
- name: TestSuite name, similar to label but without restrictions. Default is label
- cmd: Usually the command used to run the test, or any string explaining what is actually run. 
  Default is ''
- desc: Description of the testsuite. Default is ''
- filters: Filtering is used to run a subset of all tests. This field describes the used filters. 
  Default is ''


- tests: orderered sequence of all run unittests. 
  The order is just for displaying results, doesn't reflect run order
- ntests: total number of tests
- ntests_ok: number of passed tests
- ntests_ko: number of tailed tests
'''
class TSResult:

    
    def __init__(self,
                 proj_name,
                 proj_tag = 'master',
                 proj_ver = '1.0.0', proj_id='',
                 label=None,
                 name=None,
                 cmd='',
                 desc='',
                 filters=''):
        if label is None:
            label = proj_name
        if name is None:
            name = label
        
        self.proj_name = proj_name
        self.proj_tag = proj_tag
        self.proj_ver = proj_ver
        self.proj_id = proj_id
        self.label = label
        self.name = name
        self.cmd = cmd
        self.desc = desc
        self.filters = filters

        self.tests = []
        self.ntests = 0
        self.ntests_ok = 0
        self.ntests_ko = 0

    '''
    Add a unit test result
    '''
    def add_test(self, ut):
        self.tests.append(ut)
        ut.id = self.ntests

        self.ntests += 1
        if ut.valid:
            self.ntests_ok += 1
        else:
            self.ntests_ko += 1


    def valid(self):
        return self.ntests == self.ntests_ok
