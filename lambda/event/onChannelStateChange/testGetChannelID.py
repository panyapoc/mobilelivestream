def getChannelID (ChannelARN) :
    return ChannelARN.rsplit(':',1)[1]

print(getChannelID('arn:aws:medialive:ap-southeast-1:962222257213:channel:6143654'))