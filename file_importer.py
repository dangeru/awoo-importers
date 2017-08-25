import glob, subprocess, pymysql, html
def escape(x): return con.escape_string(x)
def insert_op(title, comment, board):
	comment = escape(html.unescape(comment))
	title = escape(html.unescape(title))
	res = "DELETE FROM x;\n"
	res += "INSERT INTO posts (board, title, content) VALUES ('"+board+"', '"+title+"', '"+comment+"');\n"
	res += "INSERT INTO x (id) VALUES (LAST_INSERT_ID());\n"
	return res
def insert_reply(comment, board):
	comment = escape(html.unescape(comment))
	return "INSERT INTO posts (board, content, parent) VALUES ('"+board+"', '"+comment+"', (SELECT id FROM x));\n"
con = pymysql.connect("localhost", "awoo", "awoo", "awoo")
out = open("output.sql", "w")
out.write("USE awoo;\n")
out.write("DELETE FROM posts;\n")
out.write("CREATE TEMPORARY TABLE x (id INTEGER);\n")
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
			reply += "\n" + line
	replies.append(reply)
	out.write(insert_op(title, replies[0], "tech"))
	for reply in replies[1:]:
		out.write(insert_reply(reply, "tech"))
out.write("DROP TABLE x;\n")
out.close();
