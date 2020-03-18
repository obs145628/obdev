import os

from pyutils import ioutils


'''
Dump TS results to IO files
'''
class FilesDumper:

    def __init__(self, ts, out_dir):
        self.ts = ts
        self.out_dir = out_dir

    '''
    Standard dump mode
    Write sumarry file, all valid tests in one file, all failed tests in another
    All writen in ./obts/results/
    '''
    def dump(self):
        with open(ioutils.creat_rec(os.path.join(self.out_dir, 'results/summary.txt')), 'w') as f:
            self.dump_summary(f)
        with open(ioutils.creat_rec(os.path.join(self.out_dir, 'results/valids.txt')), 'w') as f:
            self.dump_full(f, dump_kos=False)
        with open(ioutils.creat_rec(os.path.join(self.out_dir, 'results/fails.txt')), 'w') as f:
            self.dump_full(f, dump_oks=False)

    # Dump a short sumarry of all tests to the stream `os`
    def dump_summary(self, os):

        for ut in self.ts.tests:
            t_str = '{} [{}]'.format(ut.name, 'OK' if ut.valid else 'KO')
            if ut.status != '0':
                t_str += ': {}'.format(ut.status)
            t_str += '\n'

            if not ut.valid:
                t_str += ut.err_short + '\n'
                t_str += ut.err_long + '\n'

            os.write(t_str)

        total = self.ts.ntests
        succ = self.ts.ntests_ok
        perc = (succ * 100.) / total
        valid = succ == total
        os.write('\n==================\n')
        os.write('TestSuite {} !\n'.format('succeeded' if valid else 'failed'))
        os.write('# Tests  : {}\n'.format(total))
        os.write('# Passed : {}\n'.format(succ))
        os.write('# Failed : {}\n'.format(total - succ))
        os.write('Accuracy : {}%\n'.format(perc))
        os.write('==================\n')
        

    '''
    Dump all informations about every to the stream `os`
    Can choose to only dump valid or invalid tests
    '''
    def dump_full(self, os, dump_oks = True, dump_kos=True):

         for ut in self.ts.tests:
             if not dump_oks and ut.valid:
                 continue
             if not dump_kos and not ut.valid:
                 continue

             os.write('Test {} [{}]:\n'.format(ut.name, 'OK' if ut.valid else 'KO'))
             os.write('Name: {}\n'.format(ut.name))
             if ut.label != ut.name:
                 os.write('Label: {}\n'.format(ut.label))
             if len(ut.desc) != 0:
                os.write('Description: {}\n'.format(ut.desc))
             if ut.status != '0':
                os.write('Status: {}\n\n'.format(ut.status))

             os.write('OUTPUT:\n<<BEG>>>{}<<END>>\n\n'.format(ut.output))
             os.write('EXPECTED:\n<<BEG>>>{}<<END>>\n\n'.format(ut.expected))

             os.write('{}\n'.format(ut.err_short))
             os.write('{}\n\n'.format(ut.err_long))

             for key in ut.custom:
                 os.write('{}: {}\n'.format(key, ut.custom[key]))
             os.write('\n')
             
