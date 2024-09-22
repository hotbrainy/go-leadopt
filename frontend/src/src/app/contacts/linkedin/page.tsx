"use client";

import React, { useState } from "react";
import { useEffect } from "react";

import type { TableProps } from "antd";
import { Space, Table, Layout } from "antd";
import { DataType } from "@/types";
import api from "@/api";

const { Content } = Layout;

const Linkedin: React.FC = () => {
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
    api("profile").then((res) => {
      setData(res.results);
    });
  }, []);

  return (
    <Content
      style={{
        margin: "24px 16px",
        padding: 24,
        minHeight: 280,
      }}
    >
      <Table columns={columns} dataSource={data} />
    </Content>
  );
};

export default Linkedin;
