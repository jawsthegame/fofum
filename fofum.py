import argparse
import boto
import commands
import os


def display_intro():
  print '\nfofum - connect to amazon your elastic beanstalk instances'

def parse_result(result):
  rows = result.split('\n')
  info = []
  if len(rows) >= 3:
    cols = rows[0].split(' | ')
    data = [r.split(' | ') for r in rows[2:]]
    info = [dict(zip(cols, row)) for row in data]
  else:
    print 'NO DATA'
    return None

  return info

def get_input_from_choices(choices, header, entity):
  print '\n%s\n------------------------------------------------' % header
  for k, v in choices.iteritems(): print '%2s - %s' % (k, v)
  print ' 0 - exit'

  try:
    num = int(raw_input('\nChoose an %s: ' % entity))
  except:
    num = -1
    pass

  if num > 0 and num <= len(choices):
    return choices[num]
  elif num is 0:
    os._exit(0)

def get_env():
  environments = commands.getoutput(
    './aws/api/bin/elastic-beanstalk-describe-environments 2>/dev/null')

  envs = parse_result(environments)
  i = 0
  env_names = {}
  for env in envs:
    i += 1
    env_names[i] = env['EnvironmentName']

  env = None
  while not env:
    env = get_input_from_choices(env_names, 'environments:', 'environment')

  return env

def get_instance(env, ssh_args=''):
  resources = commands.getoutput(
    './aws/api/bin/elastic-beanstalk-describe-environment-resources ' + \
      '-e %s 2>/dev/null' \
      % env
  )

  info = parse_result(resources)[0]
  instances = info['Instances'].split(', ')

  ec2 = boto.connect_ec2()
  reservations = ec2.get_all_instances(instance_ids=instances)
  i = 0
  dns_names = {}

  for r in reservations:
    i += 1
    if r.instances[0].public_dns_name:
      dns_names[i] = r.instances[0].public_dns_name
    elif r.instances[0].private_ip_address:
      dns_names[i] = r.instances[0].private_ip_address

  while True:
    instance = get_input_from_choices(
      dns_names,
      'instances (%s):' % env, 'instance'
    )
    _ssh(instance, ssh_args)


def _ssh(ip='', args=''):
  user = 'ec2-user'
  if args:
    os.system('ssh %s %s@%s' % (args, user, ip))
  else:
    os.system('ssh %s@%s' % (user, ip))


def main():
  os.putenv(
    'AWS_CREDENTIAL_FILE',
    os.path.expanduser('~/.elasticbeanstalk.cfg')
  )
  parser = argparse.ArgumentParser()
  parser.add_argument('-ssh-opts', '--ssh-opts', dest='ssh_args')
  args = parser.parse_args()

  display_intro()
  env = get_env()
  get_instance(env, ssh_args=args.ssh_args)


if __name__ == "__main__":
  main()
