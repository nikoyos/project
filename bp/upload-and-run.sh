# 上传项目到服务器
scp -r . ubuntu@muziguangyu.cc:/home/ubuntu/project/bp

# 在服务器重启项目
ssh ubuntu@muziguangyu.cc 'sh /home/ubuntu/project/bp/run.sh'
