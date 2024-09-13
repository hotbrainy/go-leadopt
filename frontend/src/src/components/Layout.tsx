"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

import {
  ConfigProvider,
  Layout,
  Menu,
  Avatar,
  Button,
  theme,
  Flex,
  Dropdown,
  Affix,
} from "antd";
import type { MenuProps } from "antd";
import { WebSocketProvider } from "next-ws/client";

import { MenuInfo } from "@/types";

import {
  MoonOutlined,
  SunOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  UploadOutlined,
  SettingOutlined,
  UserOutlined,
  QuestionOutlined,
  UserSwitchOutlined,
  RedEnvelopeOutlined,
  ContactsOutlined,
  LinkedinOutlined,
  LogoutOutlined,
} from "@ant-design/icons";

const { Header, Sider } = Layout;

const sideBarItems: MenuProps["items"] = [
  {
    key: "dashboard",
    icon: <UserOutlined />,
    label: `Dashboard`,
  },
  {
    key: "contacts",
    icon: <ContactsOutlined />,
    label: `Contacts`,
    children: [
      { key: "linkedin", icon: <LinkedinOutlined />, label: "Linkedin" },
    ],
  },
  {
    key: "news",
    icon: <RedEnvelopeOutlined />,
    label: `News`,
  },
  {
    key: "leads",
    icon: <UserSwitchOutlined />,
    label: `Leads`,
  },
  {
    key: "competition",
    icon: <UploadOutlined />,
    label: `Competition`,
  },
  {
    key: "queries",
    icon: <QuestionOutlined />,
    label: `Queries`,
  },
];

const profileItems: MenuProps["items"] = [
  {
    key: "myprofile",
    icon: <UserOutlined />,
    label: `Profile`,
  },
  {
    key: "setting",
    icon: <SettingOutlined />,
    label: `Setting`,
  },
  {
    key: "logout",
    icon: <LogoutOutlined />,
    label: `Logout`,
  },
];

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const router = useRouter();
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const [collapsed, setCollapsed] = useState<boolean>(false);
  const [selectedkeys, setSelectedkeys] = useState<string[]>([]);
  const [isDarkTheme, setDarkTheme] = useState<boolean>(false);

  const onThemeChange = () => {
    if (!isDarkTheme) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    setDarkTheme(!isDarkTheme);
  };
  const onMenuClick = (e: MenuInfo) => {
    setSelectedkeys(e.keyPath);
    router.push("/" + e.keyPath.reverse().join("/"));
  };
  return (
    <ConfigProvider
      theme={{
        token: {
          borderRadius: 0,
          motion: false,
        },
        algorithm: isDarkTheme ? theme.darkAlgorithm : theme.defaultAlgorithm,
      }}
    >
      <Layout hasSider>
        <Affix offsetTop={0}>
          <Sider
            trigger={null}
            collapsible
            collapsed={collapsed}
            className="h-screen overflow-auto"
            style={{
              insetInlineStart: 0,
              scrollbarWidth: "thin",
              scrollbarColor: "unset",
            }}
          >
            <div
              className="h-16 justify-center items-center text-center p-6 cursor-pointer"
              onClick={() => {
                setSelectedkeys([]);
                router.push("/");
              }}
            >
              {collapsed ? "LO" : "LEAD OPT"}
            </div>
            <Menu
              theme="dark"
              mode="inline"
              defaultSelectedKeys={[]}
              selectedKeys={selectedkeys}
              items={sideBarItems}
              onClick={onMenuClick}
            />
          </Sider>
        </Affix>
        <Layout className="min-h-screen">
          <Header
            className="p-0 flex justify-between items-center pr-4"
            style={{ background: isDarkTheme ? "" : colorBgContainer }}
          >
            <Button
              type="text"
              icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              onClick={() => setCollapsed(!collapsed)}
              className="!w-16 h-16 text-base"
            />
            <Flex
              align="flex-end"
              justify="space-between"
              className="gap-2 items-center"
            >
              <Button
                type="text"
                icon={isDarkTheme ? <SunOutlined /> : <MoonOutlined />}
                onClick={onThemeChange}
                className="!w-16 h-16 text-base"
              />
              <Dropdown
                menu={{ items: profileItems }}
                placement="bottomRight"
                trigger={["click"]}
              >
                <Avatar icon={<UserOutlined />} className="w-12 h-12" />
              </Dropdown>
            </Flex>
          </Header>
          <WebSocketProvider url="ws://localhost:8000/">
            {children}
          </WebSocketProvider>
        </Layout>
      </Layout>
    </ConfigProvider>
  );
}
