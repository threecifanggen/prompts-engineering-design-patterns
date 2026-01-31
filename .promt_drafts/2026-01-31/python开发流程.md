
# Python 开发流程

1. 判断指定是folder还是file
    - 指定为folder的情况    
        -  读取folder里的requirements.md文件，整理需求成工作流和AI-friendly的需求，并重新覆盖
    - 指定为file的情况
        - 读取file里的file comment需求，整理需求成工作流和AI-friendly的需求，并重新覆盖
2. 根据工作流和AI-friendly的需求，生成开发流程
3. 进行开发
4. 开发结束，交由subagent @formatter 格式化代码

