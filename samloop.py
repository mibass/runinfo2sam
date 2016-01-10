import samweb_client
import datetime
from slowmondb import *
from FixedOffset import *
samweb = samweb_client.SAMWebClient(experiment='uboone')
files=samweb.listFiles("run_number 3702")

fsmcdb=smcdb()

for f in files:
  print f
  #get sam meta data for this file
  mdata=samweb.getMetadata(f)
  
  #dates from sam are formatted like 2015-11-12T12:00:06+00:00
  #put start and end into datetimes
  start= parseISOTime(mdata['start_time'])
  end= parseISOTime(mdata['end_time'])
  
  print "querying for %s to %s"%(start,end)
  
  #print fsmcdb.ChannelStatsInTimeRange('uB_ArPurity_PM01_0/LIFETIME',start,end)
  print fsmcdb.GetClosestChannelValue('uB_TPCDrift_HV01_1_0/voltage',start)
  #print fsmcdb.GetClosestChannelValue('uB_ArPurity_PM01_0/LIFETIME',end)
  
  #print fsmcdb.GetClosestChannelValue('uB_TPCDrift_HV01_1_0/voltage',datetime.datetime.now())
  exit()