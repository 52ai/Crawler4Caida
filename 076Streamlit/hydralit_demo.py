# coding: utf-8
"""
create on Jan 27, 2022 By Wayne YU

Function:

继续测试Streamlit的awsome功能
至于是否需要集成到MachineEyes项目中，则需要秉持简单有效的原则
其实测试就是在了解积木块，而构建系统，则是把这些积木块物尽其用，按照自己的想法构建不同的应用系统（用于解决不同的问题）
这个过程是非常有趣的

吴军老师说的计算机思维，可以在这个创造的过程中表现的淋漓尽致

"""
import hydralit as hy

app = hy.HydraApp(title='MachineEyes')


@app.addapp()
def my_home():
    hy.info('Hello from app1')


@app.addapp()
def app2():
    hy.info('Hello from app2')


app.run()
