import os
import sys
import boto3

def rename_file(key, backup_key, backup_strategy):
	"""
	Helper Function for put_content_to_s3 to rename file with backup key name or backup key folder

	Arguments:
		key {str} -- s3 file key
		backup_key {str} -- backup key

	Returns:
		renamed_key{str} -- renamed key
	"""
	renamed_file = key+'_'+backup_key
	try:
		file_name = os.path.basename(key)
		folder = key.split(file_name)[0]
		if backup_strategy=='file':
			if key.count('.')==1:
				file_name = file_name.split('.')[0]+'_'+backup_key+'.'+file_name.split('.')[-1]
				renamed_file =  folder+file_name
		else:
			renamed_file = "{0}{1}/{2}".format(folder, backup_key, file_name)
	except Exception as e:
		print("Error Renaming file "+str(e))
	finally:
		return renamed_file
	
def put_content_to_s3(s3_path, content, s3_client=None):
	
	return_object = {
		'success' : True,
		'data' : ''
	}
	try:
		
		#create s3 client for given s3 path
		bucket = s3_path.split('/')[2]
		key = '/'.join(s3_path.split('/')[3:])
		if not s3_client:
			s3_client_ = boto3.client(
                service_name='s3',
                aws_access_key_id='AKIASPA5YVK3TBH2ZS4H',
                aws_secret_access_key='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'
            )
		else:
			s3_client_ = s3_client

		#put current content to s3
		s3_put_response = s3_client_.put_object( Body=content, Bucket=bucket, Key=key )
		if s3_put_response['ResponseMetadata']['HTTPStatusCode']!=200:
			raise Exception('Unable to put data to s3: {0}'.format(s3_put_response))
		
	except Exception as e:
		return_object['success'] = False
		exception_message = "message: {0}\nline no:{1}\n".format(str(e),sys.exc_info()[2].tb_lineno)
		return_object['data'] = exception_message
	finally:
		return return_object