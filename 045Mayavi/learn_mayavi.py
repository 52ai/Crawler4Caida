# coding:utf-8
"""
create on June 22, 2020 By Wenyan YU

Function:
经过上周的努力，发现Python Mayavi三维绘图功能还是不错的，该程序是为了系统的学习mayavi的绘图功能

"""
import mayavi.mlab as mlab
import numpy as np
import time


def peaks(x, y):
    """
    添加matlab peaks函数
    :param x:
    :param y:
    :return:
    """
    fun_peaks = 3.0 * (1.0 - x) ** 2 * np.exp(-(x ** 2) - (y + 1.0) ** 2) - 10 * (x / 5.0 - x ** 3 - y ** 5) * np.exp(
        -x ** 2 - y ** 2) - 1.0 / 3.0 * np.exp(-(x + 1.0) ** 2 - y ** 2)
    return fun_peaks


def mayavi_barchart():
    """
    绘制barchart图
    :return:
    """
    mlab.figure(fgcolor=(0, 0, 0), bgcolor=(1, 1, 1))  # 更改背景色
    # s = np.random.rand(3, 3)
    # print(s)
    # mlab.barchart(s)
    # mlab.vectorbar()
    # mlab.show()

    x, y = np.mgrid[-5:5:20j, -5:5:20j]
    # print(x, y)
    s = peaks(x, y)
    mlab.barchart(x, y, s)
    mlab.vectorbar()
    mlab.show()


def mayavi_contour3d():
    """
    绘制contour3d图
    :return:
    """
    x, y, z = np.ogrid[-5:5:64j, -5:5:64j, -5:5:64j]
    scalars = x * x * 0.5 + y * y + z * z * 2.0
    mlab.contour3d(scalars, contours=6, transparent=True)
    mlab.colorbar()
    mlab.show()


def mayavi_contour_surf():
    """
    绘制contour_surf图
    :return:
    """
    x, y = np.mgrid[-5:5:70j, -5:5:70j]
    # 绘制peaks函数的等高线
    mlab.contour_surf(x, y, peaks, contours=9)
    mlab.colorbar()
    mlab.show()


def mayavi_imshow():
    """
    绘制mayavi imshow图
    :return:
    """
    s = np.random.rand(3, 3)  # 生成随机的3*3数组
    mlab.imshow(s)
    mlab.colorbar()
    mlab.show()


def mayavi_mesh():
    """
    绘制mayavi mesh图
    :return:
    """
    x, y = np.mgrid[-5:5:70j, -5:5:70j]
    z = peaks(x, y)
    mlab.mesh(x, y, z)
    mlab.colorbar()
    mlab.show()


def mayavi_surf():
    """
    绘制mayavi surf图
    :return:
    """
    pk_x, pk_y = np.mgrid[-5:5:70j, -5:5:70j]
    pk_z = peaks(pk_x, pk_y)
    mlab.surf(pk_z, warp_scale='auto', colormap='jet')
    mlab.colorbar()
    mlab.show()


def mayavi_plot3d():
    """
    绘制mayavi plot3d图
    :return:
    """
    t = np.mgrid[-np.pi:np.pi:100j]
    mlab.plot3d(np.cos(t), np.sin(3*t), np.cos(5*t), color=(0.23, 0.6, 1), colormap='Spectral')
    mlab.colorbar()
    mlab.show()


def mayavi_points3d():
    """
    绘制mayavi points3d
    :return:
    """
    t = np.mgrid[-np.pi:np.pi:50j]
    s = np.sin(t)
    # 参数s是设置每个点的大小(scalar), mode可选
    mlab.points3d(np.cos(t), np.sin(3*t), np.cos(5*t), s, mode='sphere', line_width=1)
    print(np.cos(t))
    mlab.colorbar()
    mlab.show()


def mayavi_quiver3d():
    """
    绘制mayavi quiver3d图
    :return:
    """
    x, y, z = np.mgrid[-0:3:0.6, -0:3:0.6, 0:3:0.3]
    print(x, y, z)
    r = np.sqrt(x**2 + y**2 + z**4)
    u = y * np.sin(r)/(r + 0.001)
    v = -x * np.sin(r) / (r + 0.001)
    w = np.zeros_like(r)
    mlab.quiver3d(x, y, z, u, v, w)
    mlab.colorbar()
    mlab.show()


def mayavi_anim():
    """
    绘制mayavi 动画
    :return:
    :return:
    """
    @mlab.animate(delay=200)  # 设置延时时间为200ms， 默认为500ms
    def my_anim():
        x, y = np.mgrid[0:3:1, 0:3:1]
        print(x, y)
        s = mlab.surf(x, y, np.asarray(x * 0.1, 'd'))
        for i in range(1000):
            s.mlab_source.scalars = np.asarray(x*0.1*(i+1), 'd')
            yield
    my_anim()
    mlab.show()


def mayavi_flow():
    """
    绘制mayavi flow图
    :return:
    """
    x, y, z = np.mgrid[-4:4:40j, -4:4:40j, 0:4:20j]
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2 + 0.1)
    u = y * np.sin(r) / r
    v = -x * np.sin(r) / r
    w = np.ones_like(z) * 0.05
    mlab.flow(u, v, w)
    mlab.show()


if __name__ == "__main__":
    time_start = time.time()  # 记录程序启动的时间
    # mayavi_barchart()
    # mayavi_contour3d()
    # mayavi_contour_surf()
    # mayavi_imshow()
    # mayavi_mesh()
    # mayavi_surf()
    # mayavi_plot3d()
    mayavi_points3d()
    # mayavi_quiver3d()
    # mayavi_anim()
    # mayavi_flow()
    time_end = time.time()  # 记录程序结束的时间
    print("\n=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
