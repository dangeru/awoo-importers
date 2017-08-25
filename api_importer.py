#!/usr/bin/env python3
import json, urllib.request, pymysql, sys, traceback, html, re
global_op_id = -100
con = pymysql.connect("localhost", "awoo", "awoo", "awoo")
boards = ["a", 
		#"lain", 
		"cyb", "d", "mu", "tech", "v", "u", "burg", "new"]
out = open("output.sql", "w")
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
out.write("USE awoo;\n")
out.write("DELETE FROM posts;\n")
global_op_id = -100
def escape(x): return con.escape_string(x)
def insert_op(title, comment, board):
	global global_op_id
	comment = escape(html.unescape(comment))
	title = escape(html.unescape(title))
	global_op_id -= 1
	return "INSERT INTO posts (post_id, board, title, content) VALUES ("+str(global_op_id)+", '"+board+"', '"+title+"', '"+comment+"');\n"
def insert_reply(op, comment, board):
	global global_op_id
	#comment = html.unescape(re.sub("\\&([0-9]{3});", "\\&#\\1;", comment))
	#comment = escape(html.unescape(comment))
	comment = escape(html.unescape(comment).replace("&039;", "'"))
	#print(comment)
	op = escape(html.unescape(op))
	return "INSERT INTO posts (board, content, parent) VALUES ('"+board+"', '"+comment+"', "+str(global_op_id)+");\n"
def request(url):
	r = urllib.request.Request(url, data = None, headers = {"User-Agent": ua})
	return urllib.request.urlopen(r).read().decode("utf-8").replace("\n", "\\n").replace("\r", "\\r")
for board in boards:
	posts = json.loads(request("https://boards.dangeru.us/api.php?type=index&board=" + board + "&ln=50"))
	for post in posts["threads"]:
		try:
			thread = json.loads(request("https://boards.dangeru.us/api.php?type=thread&board=" + board + "&thread=" + str(post["id"]) + "&ln=10000"))
			title = thread["meta"][0]["title"]
			op_comment = thread["replies"][0]["post"]
			out.write(insert_op(title, op_comment, board))
			for i in range(1, len(thread["replies"])):
				comment = thread["replies"][i]["post"]
				out.write(insert_reply(title, comment, board))
			print("Thread " + board + "/" + str(post["id"]) + " - " + post["title"] + " - Success")
		except KeyboardInterrupt:
			sys.exit(1)
		except:
			print(traceback.format_exc())
			print("Error on thread " + board + "/" + str(post["id"]) + " - " + post["title"] + " - skipping")
out.close()
