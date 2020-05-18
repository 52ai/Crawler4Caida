# coding:utf-8
"""
create on May 18, 2020 By Wenyan YU
Function:

经过几番周折，Pyecharts中的JS技术进行全球BGP网络可视化时，如果节点过万，其绘制的过程是很难容忍的
即使提前绘制好，也存在性能不足的问题。

因此PCL和Open3D框架是一个很好的突破口
二者均基于C++开发，采用并行计算框架，对大规模点云数据展示进行性能的调优，适合用于全球互联网BGP网络互联关系的展示

该程序主要是为了学习测试Open3D框架中点、线的绘制（包括位置、颜色、大小、粗细等内容）
然后再将全球互联网BGP网络互联关系数据梳理成相应的格式。
"""

import open3d as o3d
import random
import numpy as np
import csv


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csvFile = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csvFile, delimiter=" ")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


if __name__ == "__main__":
    print("Hello, Open3D! Let's draw something.")
    # 生成点云数据，[[x,y,z], ...]
    points = []
    points_list = []
    temp_list = []
    for i in range(0, 10000):
        theta = random.uniform(0, 2*np.pi)
        delta = random.uniform(0, 2*np.pi)
        # r = random.uniform(0, 100)
        r = 100

        x = r*np.sin(theta)*np.cos(delta)
        y = r*np.sin(theta)*np.sin(delta)
        z = r*np.cos(theta)
        # z = 0
        # x = random.uniform(-10, 10)  # 随机生成范围内的浮点数
        # y = random.uniform(-10, 10)  # 随机生成范围内的浮点数
        # z = random.uniform(-10, 10)  # 随机生成范围内的浮点数
        temp_list.append(x)
        temp_list.append(y)
        temp_list.append(z)
        points.append(temp_list)
        temp_list = []

    temp_list = []
    for i in range(0, len(points)):
        r = random.uniform(0, 1)  # 随机生成范围内的浮点数
        g = random.uniform(0, 1)  # 随机生成范围内的浮点数
        b = random.uniform(0, 1)  # 随机生成范围内的浮点数
        temp_list.extend(points[i])
        temp_list.append(r)
        temp_list.append(g)
        temp_list.append(b)
        points_list.append(temp_list)
        temp_list = []

    # print(points)
    save_path = "./my_points.txt"
    write_to_csv(points_list, save_path)
    lines = [[random.randint(0, len(points)-1), random.randint(0, len(points)-1)] for i in range(len(points)//10)]
    # print(lines)
    colors = [[random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)] for i in range(len(lines))]
    # colors = [[1, 0, 0] for i in range(len(lines))]
    # print(colors)
    line_set = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(points),
        lines=o3d.utility.Vector2iVector(lines)
    )
    line_set.colors = o3d.utility.Vector3dVector(colors)
    # o3d.visualization.draw_geometries([line_set], window_name='BGPVis', width=900, height=500)

    print("Let's draw some primitives")
    mesh_box = o3d.geometry.TriangleMesh.create_box(width=1,
                                                    height=1,
                                                    depth=1)
    mesh_box.compute_vertex_normals()
    mesh_box.paint_uniform_color([0, 1, 1])

    mesh_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=1.0)
    mesh_sphere.compute_vertex_normals()
    mesh_sphere.paint_uniform_color([0.1, 0.1, 0.7])

    mesh_cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=0.3,
                                                              height=4.0)
    mesh_cylinder.compute_vertex_normals()
    mesh_cylinder.paint_uniform_color([0.1, 0.9, 0.1])

    mesh_arrow = o3d.geometry.TriangleMesh.create_arrow(cylinder_radius=1.0,
                                                        cone_radius=1.5,
                                                        cylinder_height=5.0,
                                                        cone_height=4.0,
                                                        resolution=20,
                                                        cylinder_split=4,
                                                        cone_split=1)
    mesh_arrow.compute_vertex_normals()
    mesh_arrow.paint_uniform_color([0, 1, 0])

    mesh_moebius = o3d.geometry.TriangleMesh.create_moebius(length_split=70,
                                                            width_split=15,
                                                            twists=1,
                                                            raidus=1,
                                                            flatness=1,
                                                            width=1,
                                                            scale=1)
    mesh_moebius.compute_vertex_normals()
    mesh_moebius.paint_uniform_color([0, 0, 0])

    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1, origin=[-11, -11, -11])

    # o3d.visualization.draw_geometries([line_set, mesh_moebius, mesh_frame],
    #                                   window_name='BGPVis',
    #                                   width=900,
    #                                   height=500)

    pcd = o3d.io.read_point_cloud("./my_points.txt", format='xyzrgb')
    print(pcd)
    print(np.asarray(pcd.points))
    o3d.visualization.draw_geometries([pcd, line_set], window_name='BGPVis', width=900, height=500)




