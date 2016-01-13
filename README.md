fofum
=====

a quick utility for connection to elastic beanstalk instances

###Installation
Just clone this repository: <code>git clone git@github.com:jawsthegame/fofum</code>

Then you will need to install boto: <code>pip install boto</code>

###Configuration
You will need two configuration files in your home directory to use this utility.

The first is for [boto](https://github.com/boto/boto) and should have this path: <code>~/.boto</code>
<pre><code>[Credentials]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
</code></pre>

The second is for the [AWS Elastic Beanstalk CLI](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/usingCLI.html) and should have this path: <code>~/.elasticbeanstalk.cfg</code>
<pre><code>AWSAccessKeyId=YOUR_ACCESS_KEY
AWSSecretKey=YOUR_SECRET_KEY</code></pre>

You will also need to make sure the ec2-user keys associated with these instances are added:
<pre><code>ssh-add ~/.ec2/production.pem
ssh-add ~/.ec2/development.pem</code></pre>

###Usage

Once configuration is complete, you can run the script.  Your working directory must be the directory fofum.py is in: <code>python fofum.py</code>

You must first select the environment:
<pre><code>Environments:
------------------------------------------------
 1 - production
 2 - staging
 3 - development
 0 - Exit

Choose an environment:</code></pre>

Then, the instance:
<pre><code>Instances (production):
------------------------------------------------
 1 - my-1st-instance.compute-1.amazonaws.com
 2 - my-2nd-instance.compute-1.amazonaws.com
 3 - my-3rd-instance.compute-1.amazonaws.com
 4 - my-4th-instance.compute-1.amazonaws.com
 0 - Exit

Choose an instance:</code></pre>

You will then be connected to the instance using the ec2-user key you added during configuration.
