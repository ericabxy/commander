import subprocess

g_out = subprocess.run(('gsettings', 'list-schemas'), capture_output=True)
schemas = g_out.stdout.decode('utf-8').split()

for schema in schemas:
	first = schema.split('.')[0]
	print(first)
