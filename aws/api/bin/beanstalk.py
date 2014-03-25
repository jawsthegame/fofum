import boto
import commands
import os
import sys


env = sys.argv[1]

resources = commands.getoutput(
  './elastic-beanstalk-describe-environment-resources -e %s 2>/dev/null' \
    % env
)

rows = resources.split('\n')
if len(rows) is 3:
  cols = rows[0].split(' | ')
  data = rows[2].split(' | ')
  info = dict(zip(cols, data))
else:
  print 'NO DATA'

instances = info['Instances'].split(', ')

ec2 = boto.connect_ec2()

reservations = ec2.get_all_instances(instance_ids=instances)
i = 0
dns_names = {}

for r in reservations:
  i += 1
  dns_names[i] = r.instances[0].public_dns_name

while(True):
  print '\nInstances (%s):\n' % env + \
          '------------------------------------------------'
  for k, v in dns_names.iteritems(): print '%2s - %s' % (k, v)
  print ' 0 - Exit'

  num = raw_input('\nEnter instance to connect to: ')
  if num == '0': break
  os.system('ssh ec2-user@%s' % dns_names[int(num)])
