def get_process_uuid(pid):
	m = re.search(r'(?<=:)\w+[^>]', str(pid))
	return m.group(0) 