import sys

'''
Wrapper around TestSuite class
Print UniTests results to the terminal, as soon as one get added
At the end, print a sumarry of the whole tests
'''
class CLIPrinter:

    def __init__(self, ts):
        self.ts = ts

    def add_test(self, ut):
        self.ts.add_test(ut)

        t_str = '{} [{}]'.format(ut.name, 'OK' if ut.valid else 'KO')
        if ut.status != '0':
            t_str += ': {}'.format(ut.status)
        t_str += '\n'

        if not ut.valid:
            t_str += ut.err_short + '\n'
            t_str += ut.err_long + '\n'

        sys.stdout.write(t_str)
        sys.stdout.flush()

    def summary(self):
        total = self.ts.ntests
        succ = self.ts.ntests_ok
        perc = (succ * 100.) / total
        valid = succ == total

        print('\n==================')
        print('TestSuite {} !'.format('succeeded' if valid else 'failed'))
        print('# Tests  : {}'.format(total))
        print('# Passed : {}'.format(succ))
        print('# Failed : {}'.format(total - succ))
        print('Accuracy : {}%'.format(perc))
        print('==================')
        
