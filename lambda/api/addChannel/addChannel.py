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

# BOTO3
medialive = boto3.client('medialive')
mediapackage = boto3.client('mediapackage')
dynamodb = boto3.resource('dynamodb')

# ENV VAR
medialive_sg = os.environ['medialive_sg']
archive_s3 = os.environ['archive_s3']
medialive_role_arn = os.environ['medialive_role_arn']

ddb_channel = dynamodb.Table(os.environ['ddb_channel'])

def lambda_handler(event, context):

    channeluuid = str(uuid.uuid1())
    print(f'channeli is {channeluuid}')

    # 1. Create new Medialive Input
    medialive_create_input = medialive.create_input(
        Destinations=[{'StreamName': f'input{channeluuid}'},],
        InputSecurityGroups=[ medialive_sg ],
        Name=f'input{channeluuid}',
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
        Description=f'mediapackage channel {channeluuid}',
        Id=channeluuid,
    )
    mediapackage_channeluuid = channeluuid

    # 3. Create MediaPackage Distrubution
    mediapackage_create_origin_endpoint = mediapackage.create_origin_endpoint(
        # Authorization={
        #     'CdnIdentifierSecret': 'string',
        #     'SecretsRoleArn': 'string'
        # },
        ChannelId=channeluuid,
        Description=f'mediapackage HLS distibution endpoint channel {channeluuid}',
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
        Id=channeluuid,
        Origination='ALLOW',
        StartoverWindowSeconds=300,
        TimeDelaySeconds=0
    )

    print(mediapackage_create_origin_endpoint)
    mediapackage_endpoint = mediapackage_create_origin_endpoint['Url']

    # 4. Create new Medialive Channel

    medialive_destination_s3 = str(uuid.uuid4())
    medialive_destination_mediapackage = str(uuid.uuid4())

    medialive_create_channel = medialive.create_channel(
        ChannelClass='SINGLE_PIPELINE',
        Destinations=[{
            'Id': medialive_destination_s3,
            'Settings': [{
                'Url': f's3ssl://{archive_s3}/delivery/{channeluuid}/index'
            }],
            'MediaPackageSettings': []
        },
        {
            'Id': medialive_destination_mediapackage,
            'Settings': [],
            'MediaPackageSettings': [{
                'ChannelId': channeluuid
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
            'OutputGroups': [
                {
                    'OutputGroupSettings': {
                        'HlsGroupSettings': {
                            'AdMarkers': [],
                            'CaptionLanguageSetting': 'OMIT',
                            'CaptionLanguageMappings': [],
                            'HlsCdnSettings': {
                                'HlsBasicPutSettings': {
                                    'NumRetries': 10,
                                    'ConnectionRetryInterval': 1,
                                    'RestartDelay': 15,
                                    'FilecacheDuration': 300
                                }
                            },
                            'InputLossAction': 'EMIT_OUTPUT',
                            'ManifestCompression': 'NONE',
                            'Destination': {
                                'DestinationRefId': medialive_destination_s3
                            },
                            'IvInManifest': 'INCLUDE',
                            'IvSource': 'FOLLOWS_SEGMENT_NUMBER',
                            'ClientCache': 'ENABLED',
                            'TsFileMode': 'SEGMENTED_FILES',
                            'ManifestDurationFormat': 'FLOATING_POINT',
                            'SegmentationMode': 'USE_SEGMENT_DURATION',
                            'RedundantManifest': 'DISABLED',
                            'OutputSelection': 'MANIFESTS_AND_SEGMENTS',
                            'StreamInfResolution': 'INCLUDE',
                            'IFrameOnlyPlaylists': 'DISABLED',
                            'IndexNSegments': 10,
                            'ProgramDateTime': 'EXCLUDE',
                            'ProgramDateTimePeriod': 600,
                            'KeepSegments': 21,
                            'SegmentLength': 10,
                            'TimedMetadataId3Frame': 'PRIV',
                            'TimedMetadataId3Period': 10,
                            'HlsId3SegmentTagging': 'DISABLED',
                            'CodecSpecification': 'RFC_4281',
                            'DirectoryStructure': 'SINGLE_DIRECTORY',
                            'SegmentsPerSubdirectory': 10000,
                            'Mode': 'VOD'
                        }
                    },
                    'Name': 'S3VOD',
                    'Outputs': [{
                        'OutputSettings': {
                            'HlsOutputSettings': {
                                'NameModifier': 'vod',
                                'HlsSettings': {
                                    'StandardHlsSettings': {
                                        'M3u8Settings': {
                                            'AudioFramesPerPes': 4,
                                            'AudioPids': '492-498',
                                            'NielsenId3Behavior': 'NO_PASSTHROUGH',
                                            'PcrControl': 'PCR_EVERY_PES_PACKET',
                                            'PmtPid': '480',
                                            'ProgramNum': 1,
                                            'Scte35Pid': '500',
                                            'Scte35Behavior': 'NO_PASSTHROUGH',
                                            'TimedMetadataPid': '502',
                                            'TimedMetadataBehavior': 'NO_PASSTHROUGH',
                                            'VideoPid': '481'
                                        },
                                        'AudioRenditionSets': 'program_audio'
                                    }
                                },
                                'H265PackagingType': 'HVC1'
                            }
                        },
                        'OutputName': 'S3VOD_1',
                        'VideoDescriptionName': 'video_6er6o',
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
            'VideoDescriptions': [
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
                },
                {
                    'Name': 'video_6er6o',
                    'RespondToAfd': 'NONE',
                    'Sharpness': 50,
                    'ScalingBehavior': 'DEFAULT'
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
        Name=f'Channel-{channeluuid}',
        RoleArn=medialive_role_arn,
    )

    # print(medialive_create_channel)
    ChannelId = medialive_create_channel['Channel']['Id']

    #TODO ERROR handling / Retry

    ChannelItem = {
        'ChannelId' : ChannelId,
        'Streamer' : None,
        'State' : 'IDLE',
        'RTMPEndpoint' : input_endpoint,
        'MediaPackageHLSEndpoint' : mediapackage_endpoint,
        'VoDS3key' : f'delivery/{channeluuid}/'
    }

    ddb_put_item = ddb_channel.put_item(
        Item=ChannelItem
    )

    response = {
        'message' : f'added new Channel {ChannelId}',
        'channelitem' : ChannelItem
    }


    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": '*'
        },
        'body': json.dumps(response)
    }


