## Stanford Town Game

### 前置
`examples/st_game/utils/const.py`配置的为当前项目项目的存储路径，为了方便GA的前端对接数据（避免改动它那块的代码），可将`const.py`下的

```
STORAGE_PATH = ROOT_PATH.joinpath("storage")
TEMP_STORAGE_PATH = ROOT_PATH.joinpath("temp_storage")
# 更新为
STORAGE_PATH = Path("{path/to/ga/storage}")
TEMP_STORAGE_PATH = Path("{path/to/ga/temp_storage}")
```
这样可用实现不改变GA代码情况下，实现仿真数据的对接。不然得修改GA的代码来适配MG的输出路径。    

### 后端服务启动
执行入口为：`python3 run_st_game.py "Host a open lunch party at 13:00 pm" "base_the_ville_isabella_maria_klaus" "test_sim" 10`   

`idea`为用户给第一个Agent的用户心声，并通过这个心声进行传播，看最后多智能体是否达到举办、参加活动的目标。  

### 前端服务启动
进入`generative_agents/environment/frontend_server`，使用`python manage.py runserver`启动前端服务。  
访问`http://localhost:8000/simulator_home` 进入当前的仿真界面。  

## Appreciation
The reproduction work has referred the `https://github.com/joonspk-research/generative_agents`, let's make a general statement here.