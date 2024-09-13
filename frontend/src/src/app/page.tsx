"use client";

import React, { useState } from "react";
import { getData } from "@/lib";
import { useEffect } from "react";

import type { TableProps } from "antd";
import { Space, Table, Layout } from "antd";
import { DataType } from "@/types";

const { Content } = Layout;

const Home: React.FC = () => {
  const [data, setData] = useState([]);
  const columns: TableProps<DataType>["columns"] = [
    {
      title: "First Name",
      dataIndex: "first_name",
      key: "first_name",
      render: (text) => <a>{text}</a>,
    },
    {
      title: "Last Name",
      dataIndex: "last_name",
      key: "last_name",
    },
    {
      title: "Company",
      dataIndex: "company",
      key: "company",
    },
    {
      title: "Position",
      dataIndex: "position",
      key: "position",
    },
    {
      title: "Linkedin",
      dataIndex: "linkedin_url",
      key: "linkedin_url",
    },
    {
      title: "Action",
      key: "action",
      render: (_: unknown, record: { first_name: string }) => (
        <Space size="middle">
          <a>Invite {record.first_name}</a>
          <a>Delete</a>
        </Space>
      ),
    },
  ];
  useEffect(() => {
    getData().then((res) => {
      setData(res);
      console.log(res);
    });
  }, []);

  return (
    <Content
      style={{
        margin: "24px 16px",
        padding: 24,
        minHeight: 280,
        // background: colorBgContainer,
        // borderRadius: borderRadiusLG,
      }}
    >
      <Table columns={columns} dataSource={data} />
    </Content>
  );
};

export default Home;