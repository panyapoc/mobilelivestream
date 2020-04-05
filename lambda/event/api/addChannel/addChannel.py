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
medialive_role = os.environ['medialive_role']

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

    print(f'input_arn = {input_arn}')
    print(f'input_arn = {input_endpoint}')

    # 2. Create MediaPackage Channel
    # 3. Create MediaPackage Distrubution

    # mediapackage_create_channel = mediapackage.create_channel(
    #     Description=f'mediapackage channel {channelid}',
    #     Id=channelid,
    # )

    # print(mediapackage_create_channel)

    # 4. Create new Medialive Channel

    medialive_create_channel = medialive.create_channel(
        ChannelClass='SINGLE_PIPELINE',
        Destinations=[{
            'id': 'akolzu',
            'settings': [{
                'url': f's3ssl://{archive_s3}/delivery/{channelid}'
            }],
            'mediaPackageSettings': []
        },
        {
            'id': 'ipy39t',
            'settings': [],
            'mediaPackageSettings': [{
                'channelId': 'MobilePackage' #TODO getchannelId
            }]
        }
    ],
        EncoderSettings={
        'audioDescriptions': [{
                'audioTypeControl': 'FOLLOW_INPUT',
                'languageCodeControl': 'FOLLOW_INPUT',
                'name': 'audio_womwb'
            },
            {
                'audioTypeControl': 'FOLLOW_INPUT',
                'languageCodeControl': 'FOLLOW_INPUT',
                'name': 'audio_fbphv'
            }
        ],
        'captionDescriptions': [],
        'outputGroups': [{
                'outputGroupSettings': {
                    'archiveGroupSettings': {
                        'destination': {
                            'destinationRefId': 'akolzu'
                        },
                        'rolloverInterval': 300
                    }
                },
                'name': 'Archive',
                'outputs': [{
                    'outputSettings': {
                        'archiveOutputSettings': {
                            'nameModifier': '_1',
                            'containerSettings': {
                                'm2tsSettings': {
                                    'ccDescriptor': 'DISABLED',
                                    'ebif': 'NONE',
                                    'nielsenId3Behavior': 'NO_PASSTHROUGH',
                                    'programNum': 1,
                                    'patInterval': 100,
                                    'pmtInterval': 100,
                                    'pcrControl': 'PCR_EVERY_PES_PACKET',
                                    'pcrPeriod': 40,
                                    'timedMetadataBehavior': 'NO_PASSTHROUGH',
                                    'bufferModel': 'MULTIPLEX',
                                    'rateMode': 'CBR',
                                    'audioBufferModel': 'ATSC',
                                    'audioStreamType': 'DVB',
                                    'audioFramesPerPes': 2,
                                    'segmentationStyle': 'MAINTAIN_CADENCE',
                                    'segmentationMarkers': 'NONE',
                                    'ebpPlacement': 'VIDEO_AND_AUDIO_PIDS',
                                    'ebpAudioInterval': 'VIDEO_INTERVAL',
                                    'esRateInPes': 'EXCLUDE',
                                    'arib': 'DISABLED',
                                    'aribCaptionsPidControl': 'AUTO',
                                    'absentInputAudioBehavior': 'ENCODE_SILENCE',
                                    'pmtPid': '480',
                                    'videoPid': '481',
                                    'audioPids': '482-498',
                                    'dvbTeletextPid': '499',
                                    'dvbSubPids': '460-479',
                                    'scte27Pids': '450-459',
                                    'scte35Pid': '500',
                                    'scte35Control': 'NONE',
                                    'klv': 'NONE',
                                    'klvDataPids': '501',
                                    'timedMetadataPid': '502',
                                    'etvPlatformPid': '504',
                                    'etvSignalPid': '505',
                                    'aribCaptionsPid': '507'
                                }
                            }
                        }
                    },
                    'outputName': 'Archive_1',
                    'videoDescriptionName': 'video_liuejc',
                    'audioDescriptionNames': [
                        'audio_womwb'
                    ],
                    'captionDescriptionNames': []
                }]
            },
            {
                'outputGroupSettings': {
                    'mediaPackageGroupSettings': {
                        'destination': {
                            'destinationRefId': 'ipy39t'
                        }
                    }
                },
                'name': 'MobilePackage',
                'outputs': [{
                    'outputSettings': {
                        'mediaPackageOutputSettings': {}
                    },
                    'outputName': 'MobilePackage_1',
                    'videoDescriptionName': 'video_wz2iqp',
                    'audioDescriptionNames': [
                        'audio_fbphv'
                    ],
                    'captionDescriptionNames': []
                }]
            }
        ],
        'timecodeConfig': {
            'source': 'EMBEDDED'
        },
        'videoDescriptions': [{
                'codecSettings': {
                    'h264Settings': {
                        'afdSignaling': 'NONE',
                        'colorMetadata': 'INSERT',
                        'adaptiveQuantization': 'MEDIUM',
                        'entropyEncoding': 'CABAC',
                        'flickerAq': 'ENABLED',
                        'framerateControl': 'INITIALIZE_FROM_SOURCE',
                        'gopBReference': 'DISABLED',
                        'gopClosedCadence': 1,
                        'gopNumBFrames': 2,
                        'gopSize': 90,
                        'gopSizeUnits': 'FRAMES',
                        'subgopLength': 'FIXED',
                        'scanType': 'PROGRESSIVE',
                        'level': 'H264_LEVEL_AUTO',
                        'lookAheadRateControl': 'MEDIUM',
                        'numRefFrames': 1,
                        'parControl': 'INITIALIZE_FROM_SOURCE',
                        'profile': 'MAIN',
                        'rateControlMode': 'CBR',
                        'syntax': 'DEFAULT',
                        'sceneChangeDetect': 'ENABLED',
                        'spatialAq': 'ENABLED',
                        'temporalAq': 'ENABLED',
                        'timecodeInsertion': 'DISABLED'
                    }
                },
                'name': 'video_liuejc',
                'respondToAfd': 'NONE',
                'sharpness': 50,
                'scalingBehavior': 'DEFAULT'
            },
            {
                'codecSettings': {
                    'h264Settings': {
                        'afdSignaling': 'NONE',
                        'colorMetadata': 'INSERT',
                        'adaptiveQuantization': 'MEDIUM',
                        'bitrate': 8000000,
                        'entropyEncoding': 'CABAC',
                        'flickerAq': 'ENABLED',
                        'framerateControl': 'SPECIFIED',
                        'framerateNumerator': 30,
                        'framerateDenominator': 1,
                        'gopBReference': 'DISABLED',
                        'gopClosedCadence': 1,
                        'gopNumBFrames': 2,
                        'gopSize': 90,
                        'gopSizeUnits': 'FRAMES',
                        'subgopLength': 'FIXED',
                        'scanType': 'PROGRESSIVE',
                        'level': 'H264_LEVEL_AUTO',
                        'lookAheadRateControl': 'MEDIUM',
                        'numRefFrames': 1,
                        'parControl': 'SPECIFIED',
                        'parNumerator': 1,
                        'parDenominator': 1,
                        'profile': 'MAIN',
                        'rateControlMode': 'CBR',
                        'syntax': 'DEFAULT',
                        'sceneChangeDetect': 'ENABLED',
                        'spatialAq': 'ENABLED',
                        'temporalAq': 'ENABLED',
                        'timecodeInsertion': 'DISABLED'
                    }
                },
                'height': 1080,
                'name': 'video_wz2iqp',
                'respondToAfd': 'NONE',
                'sharpness': 50,
                'scalingBehavior': 'DEFAULT',
                'width': 1920
            }
        ]
    },
        InputAttachments=[
            {
                'AutomaticInputFailoverSettings': {
                    'InputPreference': 'EQUAL_INPUT_PREFERENCE'|'PRIMARY_INPUT_PREFERRED',
                    'SecondaryInputId': 'string'
                },
                'InputAttachmentName': 'string',
                'InputId': 'string',
                'InputSettings': {
                    'AudioSelectors': [
                        {
                            'Name': 'string',
                            'SelectorSettings': {
                                'AudioLanguageSelection': {
                                    'LanguageCode': 'string',
                                    'LanguageSelectionPolicy': 'LOOSE'|'STRICT'
                                },
                                'AudioPidSelection': {
                                    'Pid': 123
                                }
                            }
                        },
                    ],
                    'CaptionSelectors': [
                        {
                            'LanguageCode': 'string',
                            'Name': 'string',
                            'SelectorSettings': {
                                'AribSourceSettings': {}
                                ,
                                'DvbSubSourceSettings': {
                                    'Pid': 123
                                },
                                'EmbeddedSourceSettings': {
                                    'Convert608To708': 'DISABLED'|'UPCONVERT',
                                    'Scte20Detection': 'AUTO'|'OFF',
                                    'Source608ChannelNumber': 123,
                                    'Source608TrackNumber': 123
                                },
                                'Scte20SourceSettings': {
                                    'Convert608To708': 'DISABLED'|'UPCONVERT',
                                    'Source608ChannelNumber': 123
                                },
                                'Scte27SourceSettings': {
                                    'Pid': 123
                                },
                                'TeletextSourceSettings': {
                                    'PageNumber': 'string'
                                }
                            }
                        },
                    ],
                    'DeblockFilter': 'DISABLED'|'ENABLED',
                    'DenoiseFilter': 'DISABLED'|'ENABLED',
                    'FilterStrength': 123,
                    'InputFilter': 'AUTO'|'DISABLED'|'FORCED',
                    'NetworkInputSettings': {
                        'HlsInputSettings': {
                            'Bandwidth': 123,
                            'BufferSegments': 123,
                            'Retries': 123,
                            'RetryInterval': 123
                        },
                        'ServerValidation': 'CHECK_CRYPTOGRAPHY_AND_VALIDATE_NAME'|'CHECK_CRYPTOGRAPHY_ONLY'
                    },
                    'SourceEndBehavior': 'CONTINUE'|'LOOP',
                    'VideoSelector': {
                        'ColorSpace': 'FOLLOW'|'REC_601'|'REC_709',
                        'ColorSpaceUsage': 'FALLBACK'|'FORCE',
                        'SelectorSettings': {
                            'VideoSelectorPid': {
                                'Pid': 123
                            },
                            'VideoSelectorProgramId': {
                                'ProgramId': 123
                            }
                        }
                    }
                }
            },
        ],
        InputSpecification={
            'codec': 'HEVC',
            'resolution': 'HD',
            'maximumBitrate': 'MAX_50_MBPS'
        },
        LogLevel='DISABLED',
        Name=f'Channel{channelid}',
        RoleArn=medialive_role,
    )




    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


