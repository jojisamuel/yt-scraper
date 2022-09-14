from sqlalchemy import create_engine
import pymongo

yt = 'AIzaSyCp74eFse75Y0T2YLzRDAk3PARax_BlLfw'
my_conn = create_engine("mysql+pymysql://root:AssignmentN@35.202.167.193/yt-proj?charset=utf8mb4")
client = pymongo.MongoClient("mongodb+srv://jojis:SHvD4rRvcTi6wwox@cluster0.wj6gl.mongodb.net/?retryWrites=true&w=majority")
headers = {"Authorization": "Bearer ya29.a0AVA9y1vtdrZK0J8YTt4SQbmcNEOTebhdNXVkNuhJdUEBBSS2M3INmGazXltLyFuibCRzm1gyxUB4F_wPqjFAYxG62SoK3j58LwdIgsWGUoCn36sGg57kr2mySfk68ufZaSMz6ktIlvnTTKsuXrQbVmjKP1O2aCgYKATASARISFQE65dr83S6XBHZwUVDKWvHSPu7q8w0163"}
