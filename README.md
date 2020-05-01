# zabbix_add_host
使用zabbix API接口批量导入主机

## 一、安装第三方库
`pip install requests xlrd`

## 二、excel主机模板格式
|  Hostname | Visible | IP | Group | Templatel | SN |
|  ----  | ----  |  ----  | ----  |  ----  | ----  |
|  server1 | 服务器1 | 10.1.1.1 | Product | Template Module ICMP Ping | 2102359545619 |
|  server2 | 服务器2 | 10.1.1.2 | Product | Template Module ICMP Ping | 2105436435191 |