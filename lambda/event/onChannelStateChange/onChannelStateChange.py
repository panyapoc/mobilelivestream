# CloudWatch Channel State Change Event idle -> Running
# 1. Update Channel Status on DDB
# 2. Notify Mobile Channel Ready

# CloudWatch Channel State Change Event Running -> Idle
# 1. Update Channel Status on DDB
# 2. Start moving archive file to new location
# 3. Create .m3u8 file from list of .ts file
# 4. Add new .m3u8 to DDB for future playing
