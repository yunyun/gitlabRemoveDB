import os
import requests
import subprocess

# GitLab API 的基础 URL（替换为你的 GitLab 实例的 URL）
gitlab_url = 'http://<server>/api/v4/projects'
# 你的 GitLab 访问令牌（需要具有读取项目列表的权限）
private_token = ''
# 克隆到本地的目录
clone_directory = '/work/git/directory'

# 设置请求头
headers = {
    'PRIVATE-TOKEN': private_token
}
 
# 用于存储所有项目的列表
all_projects = []
 
# 初始化分页参数
page = 1
per_page = 100  # 你可以根据需要调整每页返回的项目数量，最大值为 100

# 构造带有分页参数的 URL
paged_url = f"{gitlab_url}?page={page}&per_page={per_page}"

while True:
    # 获取当前页的项目列表
    response = requests.get(paged_url, headers=headers)
    projects = response.json()
    
    # 将当前页的项目添加到总列表中
    all_projects.extend(projects)
    
    # 检查是否还有下一页
    links = response.headers.get('Link', '').split(',')
    
    for link in links:
        print(link)
        if 'rel="next"' in link:
            # 提取下一页的 URL
            next_page_url = link.split(';')[0][1:-1]
            paged_url = next_page_url
            # print(next_page_url)
            # 尝试从 URL 中提取页码
            page_param = next_page_url.split('=')[-1]
            # 检查页码是否是数字
            #print(page_param)
            if page_param.isdigit():
                page = int(page_param)
                break
            else:
                # 如果页码不是数字，则意味着没有更多页面
                break
    else:
        # 如果没有找到下一页的链接，则退出循环
        break


# 遍历项目列表并克隆
for project in all_projects:
    # print(project["ssh_url_to_repo"])
    # 获取项目的 HTTP 克隆 URL（你可以根据需要选择 SSH 或其他方式）
    clone_url = project['ssh_url_to_repo']
    # 获取项目的名称（用于创建本地目录）
    project_name = project['path_with_namespace'].replace('/', '-')
    # 构建本地克隆目录
    local_dir = os.path.join(clone_directory, project_name)
    
    # 如果目录不存在，则创建
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    
    # 克隆项目到本地目录
    subprocess.run(['git', 'clone', clone_url, local_dir])

print("所有项目已克隆到本地目录。")
