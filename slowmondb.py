import psycopg2
import psycopg2.extras
import time
import datetime

#note: ssh tunnel must be setup with ssh -N -f -L 1111:smc-priv:5432 ubdaq-prod-ws01

class smcdb(object):

  def __init__(self):
    self.conn = psycopg2.connect(port="1111", host="localhost", user="smcreader", database="slowmoncon_archive")
    #self.cur = self.conn.cursor()
    self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  
  def QueryToDict(self,qry,parms):
    #execute query and return a dict
    self.cur.execute(qry,parms)
    ans =self.cur.fetchall()
    dict_result = []
    for row in ans:
      dict_result.append(dict(row))
    
    return dict_result
    
  def ChannelStatsInTimeRange(self,channelname,start,end):
    return self.QueryToDict("select avg(float_val),min(float_val),max(float_val),stddev(float_val) from sample "
	  "where channel_id = (select channel_id from channel where name = %s)"
	  "and smpl_time > %s and smpl_time < %s;",
		(channelname, start, end) )

  def GetClosestChannelValue(self,channelname,dt):
    #find channel value closest to dt
    return self.QueryToDict("select float_val,smpl_time,smpl_time - date %s as age from sample "
	  "where channel_id = (select channel_id from channel where name = %s) and smpl_time > date %s "
	  "order by abs(extract(epoch from smpl_time - date %s)) "
	  "limit 1",(dt, channelname, dt, dt) )
