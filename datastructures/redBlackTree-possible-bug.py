from redBlackTree import rbtree, rbnode

def bookid2key(bookid):
	# "AZ1234" => 71855628235572
	# simple unique encoding for each book id
	return int(bookid.encode("hex"), 16)

t = rbtree()
t.insert_key( bookid2key("AB1131") )
t.insert_key( bookid2key("AB1132") )
t.insert_key( bookid2key("AB1133") )
t.insert_key( bookid2key("AB1134") )
t.insert_key( bookid2key("AB1135") )
t.insert_key( bookid2key("ZA1131") )
t.insert_key( bookid2key("ZB1131") )
t.insert_key( bookid2key("ZC1131") )
t.insert_key( bookid2key("ZD1131") )
t.insert_key( bookid2key("ZE1131") )

t.delete_key( bookid2key("AB1133") )


