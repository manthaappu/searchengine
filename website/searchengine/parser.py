

def operation(text,t1,t2,n):
	a = text.find(t1)
	b = text.find(t2)
	
	name = text[a+n:b]
	text = text[b+n:]
	return name,text
	
def write_to_file(doc_id,title,data):
	with open(str(doc_id)+'.html','w') as f_id:
		f_id.write('<html> <head> <title>')
		f_id.write(title)
		f_id.write('</title></head><body>')
		f_id.write(data)
		f_id.write('</body> </html>')
	
	#f_id.closed()
	
	


if __name__ == '__main__':
	f = open('testCollection.dat','rb')
	text = ''
	for i in f.readlines():
		text = text+i

	while text:
		
		doc_id,text = operation(text,'<id>','</id>',4)
		title,text = operation(text,'<title>','</title>',7)
		data,text = operation(text,'<text>','</text>',6)
		index = text.find('<page>')		  	
		text = text[index:]
		write_to_file(doc_id,title,data)
