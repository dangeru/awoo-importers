import glob, subprocess, pymysql, html, os, time
def escape(x): return con.escape_string(x)
def insert_op(title, comment, board, date):
	comment = escape(html.unescape(comment))
	title = escape(html.unescape(title))
	res = "DELETE FROM x;\n"
	res += "INSERT INTO posts (board, title, content, date_posted, last_bumped) VALUES ('"+board+"', '"+title+"', '"+comment+"', TIMESTAMP('"+date+"'), TIMESTAMP('"+date+"'));\n"
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
for board in glob.glob("*"):
	if not os.path.isdir(board): continue
	for f in glob.glob(board + "/thread/*.txt"):
		date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.stat(f).st_mtime))
		f = open(f, "r").read().split("\n")
		title = f[0][3:]
		f[1] = "#" + f[1][2:]
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
		out.write(insert_op(title, replies[1], board, date))
		for reply in replies[2:]:
			out.write(insert_reply(reply, board))
out.write("DROP TABLE x;\n")
out.close();
