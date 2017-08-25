import glob, subprocess, pymysql, html
global_op_id = -100
def escape(x): return con.escape_string(x)
def insert_op(title, comment, board):
	global global_op_id
	comment = escape(html.unescape(comment))
	title = escape(html.unescape(title))
	global_op_id -= 1
	return "INSERT INTO posts (post_id, board, title, content) VALUES ("+str(global_op_id)+", '"+board+"', '"+title+"', '"+comment+"');\n"
def insert_reply(comment, board):
	global global_op_id
	#comment = escape(html.unescape(comment).replace("&039;", "'"))
	comment = escape(html.unescape(comment))
	return "INSERT INTO posts (board, content, parent) VALUES ('"+board+"', '"+comment+"', "+str(global_op_id)+");\n"
con = pymysql.connect("localhost", "awoo", "awoo", "awoo")
out = open("output.sql", "w")
out.write("USE awoo;\n")
out.write("DELETE FROM posts;\n")
for f in glob.glob("threads/*.txt"):
	f = open(f, "r").read().split("\n")
	title = f[0][3:]
	f[1] = "#" + f[1][3:]
	i = 1
	replies = []
	reply = ""
	for line in f[1:]:
		if len(line) == 0: continue
		if line[0] == "#":
			replies.append(reply)
			reply = line[1:]
		else:
			reply += line
	replies.append(reply)
	out.write(insert_op(title, replies[0], "tech"))
	for reply in replies[1:]:
		out.write(insert_reply(reply, "tech"))
