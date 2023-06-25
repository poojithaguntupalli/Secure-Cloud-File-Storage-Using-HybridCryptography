import os
import shutil

NO_FILE = 'No File Selected'
INVALID_FILE = 'Invalid File Format'
NO_PART = 'No file part'

def empFolder(directory_name):
	if not os.path.isdir(directory_name):
		os.makedirs(directory_name)
	else:
		folder = directory_name
		for the_file in os.listdir(folder):
			file_path = os.path.join(folder, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path): shutil.rmtree(file_path)
			except Exception as e:
				print(e)


def filesDivide():
	empFolder('files')
	empFolder('data_storage')
	upload_file = os.listdir('uploads')
	upload_file = './uploads/'+upload_file[0]

	maxsize  = 1024*32						# 1	MB	-	max chapter size
	bufsize  = 50*1024*1024*1024  			# 50GB	-	memory buffer size

	chunks = 0
	b  = ''
	metaData = open('data_storage/metaData.txt','w')
	f1 = upload_file.split('/')
	f1 = f1[-1]
	print(f1)
	metaData.write("File_Name=%s\n" % (f1))
	with open(upload_file, 'rb') as s:
		while True:
			trgtFile = open('files/SECRET' + '%07d' % chunks, 'wb')
			g = 0
			while g < maxsize:
				if len(b) > 0:
					trgtFile.write(b)
				trgtFile.write(s.read(min(bufsize, maxsize - g)))
				g += min(bufsize, maxsize - g)
				b = s.read(1)
				if len(b) == 0:
					break
			trgtFile.close()
			if len(b) == 0:
				break
			chunks += 1
	metaData.write("chapters=%d" % (chunks+1))
	metaData.close()

def restoreFiles():
    empFolder('restored_file')

    metaData = open('data_storage/metaData.txt', 'r')
    meta_info = []
    for line in metaData:
        data = line.split('\n')[0].split('=')
        meta_info.append(data[1])
    dirPath = 'restored_file/' + meta_info[0]

    files = sorted(os.listdir('files'))

    with open(dirPath, 'wb') as writer:
        for file in files:
            path = 'files/' + file
            with open(path, 'rb') as reader:
                for line in reader:
                    writer.write(line)
                reader.close()
        writer.close()

    empFolder('files')
