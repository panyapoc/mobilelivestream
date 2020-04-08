# API - null
# 1. Create new Medialive Input
# 2. Create MediaPackage Channel
# 3. Create MediaPackage Distrubution
# 4. Create new Medialive Channel
# 5. Save Channel Detail to DDB

import boto3
import json
import uuid
import os

medialive = boto3.client('medialive')
mediapackage = boto3.client('mediapackage')

medialive_sg = os.environ['medialive_sg']
archive_s3 = os.environ['archive_s3']
medialive_role_arn = os.environ['medialive_role_arn']

def lambda_handler(event, context):

    channelid = str(uuid.uuid1())
    print(f'channeli is {channelid}')

    # 1. Create new Medialive Input
    medialive_create_input = medialive.create_input(
        Destinations=[{'StreamName': f'input{channelid}'},],
        InputSecurityGroups=[ medialive_sg ],
        Name=f'input{channelid}',
        Type='RTMP_PUSH'
    )

    input_arn = medialive_create_input['Input']['Arn']
    input_endpoint = medialive_create_input['Input']['Destinations'][0]['Url']
    input_name = medialive_create_input['Input']['Name']
    input_id = medialive_create_input['Input']['Id']

    print(f'input_arn = {input_arn}')
    print(f'input_endpoint = {input_endpoint}')
    print(f'input_name = {input_name}')
    print(f'input_id = {input_id}')

    # 2. Create MediaPackage Channel

    mediapackage_create_channel = mediapackage.create_channel(
        Description=f'mediapackage channel {channelid}',
        Id=channelid,
    )

    # print(mediapackage_create_channel)
    mediapackage_channelid = channelid

    # 3. Create MediaPackage Distrubution
    mediapackage_create_channel = mediapackage.create_origin_endpoint(
        # Authorization={
        #     'CdnIdentifierSecret': 'string',
        #     'SecretsRoleArn': 'string'
        # },
        ChannelId=channelid,
        Description=f'mediapackage HLS distibution endpoint channel {channelid}',
        HlsPackage={
            'AdMarkers': 'NONE',
            'IncludeIframeOnlyStream': False,
            'PlaylistType': 'EVENT',
            'PlaylistWindowSeconds': 60,
            'SegmentDurationSeconds': 6,
            'StreamSelection': {
                'StreamOrder': 'ORIGINAL'
            }
        },
        Id=channelid,
        Origination='ALLOW',
        StartoverWindowSeconds=300,
        TimeDelaySeconds=0
    )

    # 4. Create new Medialive Channel

    medialive_destination_s3 = str(uuid.uuid4())
    medialive_destination_mediapackage = str(uuid.uuid4())

    medialive_create_channel = medialive.create_channel(
        ChannelClass='SINGLE_PIPELINE',
        Destinations=[{
            'Id': medialive_destination_s3,
            'Settings': [{
                'Url': f's3ssl://{archive_s3}/delivery/{channelid}'
            }],
            'MediaPackageSettings': []
        },
        {
            'Id': medialive_destination_mediapackage,
            'Settings': [],
            'MediaPackageSettings': [{
                'ChannelId': channelid
            }]
        }],
        EncoderSettings={
            'AudioDescriptions': [{
                    'AudioTypeControl': 'FOLLOW_INPUT',
                    'LanguageCodeControl': 'FOLLOW_INPUT',
                    'AudioSelectorName' : 'audio_1',
                    'Name': 'audio_1'
                },
                {
                    'AudioTypeControl': 'FOLLOW_INPUT',
                    'LanguageCodeControl': 'FOLLOW_INPUT',
                    'AudioSelectorName' : 'audio_2',
                    'Name': 'audio_2'
                }
            ],
            'CaptionDescriptions': [],
            'OutputGroups': [{
                    'OutputGroupSettings': {
                        'ArchiveGroupSettings': {
                            'Destination': {
                                'DestinationRefId': medialive_destination_s3
                            },
                            'RolloverInterval': 300
                        }
                    },
                    'Name': 'Archive',
                    'Outputs': [{
                        'OutputSettings': {
                            'ArchiveOutputSettings': {
                                'NameModifier': '_1',
                                'ContainerSettings': {
                                    'M2tsSettings': {
                                        'CcDescriptor': 'DISABLED',
                                        'Ebif': 'NONE',
                                        'NielsenId3Behavior': 'NO_PASSTHROUGH',
                                        'ProgramNum': 1,
                                        'PatInterval': 100,
                                        'PmtInterval': 100,
                                        'PcrControl': 'PCR_EVERY_PES_PACKET',
                                        'PcrPeriod': 40,
                                        'TimedMetadataBehavior': 'NO_PASSTHROUGH',
                                        'BufferModel': 'MULTIPLEX',
                                        'RateMode': 'CBR',
                                        'AudioBufferModel': 'ATSC',
                                        'AudioStreamType': 'DVB',
                                        'AudioFramesPerPes': 2,
                                        'SegmentationStyle': 'MAINTAIN_CADENCE',
                                        'SegmentationMarkers': 'NONE',
                                        'EbpPlacement': 'VIDEO_AND_AUDIO_PIDS',
                                        'EbpAudioInterval': 'VIDEO_INTERVAL',
                                        'EsRateInPes': 'EXCLUDE',
                                        'Arib': 'DISABLED',
                                        'AribCaptionsPidControl': 'AUTO',
                                        'AbsentInputAudioBehavior': 'ENCODE_SILENCE',
                                        'PmtPid': '480',
                                        'VideoPid': '481',
                                        'AudioPids': '482-498',
                                        'DvbTeletextPid': '499',
                                        'DvbSubPids': '460-479',
                                        'Scte27Pids': '450-459',
                                        'Scte35Pid': '500',
                                        'Scte35Control': 'NONE',
                                        'Klv': 'NONE',
                                        'KlvDataPids': '501',
                                        'TimedMetadataPid': '502',
                                        'EtvPlatformPid': '504',
                                        'EtvSignalPid': '505',
                                        'AribCaptionsPid': '507'
                                    }
                                }
                            }
                        },
                        'OutputName': 'Archive_1',
                        'VideoDescriptionName': 'video_liuejc',
                        'AudioDescriptionNames': [
                            'audio_1'
                        ],
                        'CaptionDescriptionNames': []
                    }]
                },
                {
                    'OutputGroupSettings': {
                        'MediaPackageGroupSettings': {
                            'Destination': {
                                'DestinationRefId': medialive_destination_mediapackage
                            }
                        }
                    },
                    'Name': 'MobilePackage',
                    'Outputs': [{
                        'OutputSettings': {
                            'MediaPackageOutputSettings': {}
                        },
                        'OutputName': 'MobilePackage_1',
                        'VideoDescriptionName': 'video_wz2iqp',
                        'AudioDescriptionNames': [
                            'audio_2'
                        ],
                        'CaptionDescriptionNames': []
                    }]
                }
            ],
            'TimecodeConfig': {
                'Source': 'EMBEDDED'
            },
            'VideoDescriptions': [{
                    'CodecSettings': {
                        'H264Settings': {
                            'AfdSignaling': 'NONE',
                            'ColorMetadata': 'INSERT',
                            'AdaptiveQuantization': 'MEDIUM',
                            'EntropyEncoding': 'CABAC',
                            'FlickerAq': 'ENABLED',
                            'FramerateControl': 'INITIALIZE_FROM_SOURCE',
                            'GopBReference': 'DISABLED',
                            'GopClosedCadence': 1,
                            'GopNumBFrames': 2,
                            'GopSize': 90,
                            'GopSizeUnits': 'FRAMES',
                            'SubgopLength': 'FIXED',
                            'ScanType': 'PROGRESSIVE',
                            'Level': 'H264_LEVEL_AUTO',
                            'LookAheadRateControl': 'MEDIUM',
                            'NumRefFrames': 1,
                            'ParControl': 'INITIALIZE_FROM_SOURCE',
                            'Profile': 'MAIN',
                            'RateControlMode': 'CBR',
                            'Syntax': 'DEFAULT',
                            'SceneChangeDetect': 'ENABLED',
                            'SpatialAq': 'ENABLED',
                            'TemporalAq': 'ENABLED',
                            'TimecodeInsertion': 'DISABLED'
                        }
                    },
                    'Name': 'video_liuejc',
                    'RespondToAfd': 'NONE',
                    'Sharpness': 50,
                    'ScalingBehavior': 'DEFAULT'
                },
                {
                    'CodecSettings': {
                        'H264Settings': {
                            'AfdSignaling': 'NONE',
                            'ColorMetadata': 'INSERT',
                            'AdaptiveQuantization': 'MEDIUM',
                            'Bitrate': 8000000,
                            'EntropyEncoding': 'CABAC',
                            'FlickerAq': 'ENABLED',
                            'FramerateControl': 'SPECIFIED',
                            'FramerateNumerator': 30,
                            'FramerateDenominator': 1,
                            'GopBReference': 'DISABLED',
                            'GopClosedCadence': 1,
                            'GopNumBFrames': 2,
                            'GopSize': 90,
                            'GopSizeUnits': 'FRAMES',
                            'SubgopLength': 'FIXED',
                            'ScanType': 'PROGRESSIVE',
                            'Level': 'H264_LEVEL_AUTO',
                            'LookAheadRateControl': 'MEDIUM',
                            'NumRefFrames': 1,
                            'ParControl': 'SPECIFIED',
                            'ParNumerator': 1,
                            'ParDenominator': 1,
                            'Profile': 'MAIN',
                            'RateControlMode': 'CBR',
                            'Syntax': 'DEFAULT',
                            'SceneChangeDetect': 'ENABLED',
                            'SpatialAq': 'ENABLED',
                            'TemporalAq': 'ENABLED',
                            'TimecodeInsertion': 'DISABLED'
                        }
                    },
                    'Height': 1080,
                    'Name': 'video_wz2iqp',
                    'RespondToAfd': 'NONE',
                    'Sharpness': 50,
                    'ScalingBehavior': 'DEFAULT',
                    'Width': 1920
                }
            ]
        },
        InputAttachments=[
            {
                'InputAttachmentName': input_name,
                'InputId': input_id,
                'InputSettings': {
                    'SourceEndBehavior': 'CONTINUE',
                    'InputFilter': 'AUTO',
                    'FilterStrength': 1,
                    'DeblockFilter': 'DISABLED',
                    'DenoiseFilter': 'DISABLED',
                    'AudioSelectors': [],
                    'CaptionSelectors': []
                }
            },
        ],
        InputSpecification={
            'Codec': 'HEVC',
            'Resolution': 'HD',
            'MaximumBitrate': 'MAX_50_MBPS'
        },
        LogLevel='DISABLED',
        Name=f'Channel-{channelid}',
        RoleArn=medialive_role_arn,
    )

    print(medialive_create_channel)

    #TODO
    # ERROR handling / Retry
    # Channel Metadata to DDB


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


