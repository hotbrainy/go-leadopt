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
  SettingOutlined,
  UserOutlined,
  LinkedinOutlined,
  LogoutOutlined,
} from "@ant-design/icons";

import {
  BsRobot,
  BsSpeedometer2,
  BsShield,
  BsPersonLinesFill,
  BsNewspaper,
  BsCheck2Square,
  BsPeopleFill,
} from "react-icons/bs";
import Image from "next/image";
import Logo from "../assets/img/aelogowhite.webp";

const { Header, Sider } = Layout;

const sideBarItems: MenuProps["items"] = [
  {
    key: "home",
    icon: <BsRobot />,
    label: `Home`,
  },
  {
    key: "dashboard",
    icon: <BsSpeedometer2 />,
    label: `Dashboard`,
  },
  {
    key: "competition",
    icon: <BsShield />,
    label: `Competition`,
  },
  {
    key: "contacts",
    icon: <BsPersonLinesFill />,
    label: `Contacts`,
    children: [
      { key: "linkedin", icon: <LinkedinOutlined />, label: "Linkedin" },
    ],
  },
  {
    key: "news",
    icon: <BsNewspaper />,
    label: `News`,
  },
  {
    key: "tasks",
    icon: <BsCheck2Square />,
    label: `Tasks`,
  },
  {
    key: "leads",
    icon: <BsPeopleFill />,
    label: `Leads`,
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
              className="h-16 justify-center items-center text-center p-6 cursor-pointer flex"
              onClick={() => {
                setSelectedkeys([]);
                router.push("/");
              }}
            >
              <Image src={Logo} alt="L" width={76} height={61} />
            </div>
            <Menu
              theme="dark"
              mode="inline"
              defaultSelectedKeys={["home"]}
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
