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
  Drawer,
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
import LayoutContext from "@/contexts/LayoutContextProvider";
import { wsURL } from "@/api";
 
import ProfileImage from "../assets/avatars/nic.webp";

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
    key: "contacts",
    icon: <BsPersonLinesFill />,
    label: `Contacts`,
    children: [
      { key: "linkedin", icon: <LinkedinOutlined />, label: "Linkedin" },
    ],
  },
  {
    key: "leads",
    icon: <BsPeopleFill />,
    label: `Leads`,
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
    key: "competition",
    icon: <BsShield />,
    label: `Competition`,
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
  const [selectedkeys, setSelectedkeys] = useState<string[]>(["home"]);
  const [isDarkTheme, setDarkTheme] = useState<boolean>(true);

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
  const renderMenu = () => {
    return (
      <>
        <div
          className="h-40 justify-center items-center text-center p-6 cursor-pointer flex"
          onClick={() => {
            setSelectedkeys(["home"]);
            router.push("/home");
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
      </>
    );
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
      <LayoutContext.Provider value={{ collapsed, setCollapsed }}>
        <WebSocketProvider url={wsURL}>
          <Layout hasSider>
            <Affix offsetTop={0}>
              <>
                <Drawer
                  title=""
                  placement={"left"}
                  closable={false}
                  onClose={() => setCollapsed(false)}
                  open={collapsed}
                  key={"left"}
                  size="default"
                  rootClassName="xs:inline-block md:hidden"
                  classNames={{
                    content: "p-0 !bg-[#001529]",
                    body: "!p-0",
                  }}
                  onClick={() => setCollapsed(false)}
                >
                  {renderMenu()}
                </Drawer>
                <Sider
                  trigger={null}
                  // collapsible
                  collapsed={collapsed}
                  className="h-screen overflow-auto hidden md:inline-block"
                  style={{
                    insetInlineStart: 0,
                    scrollbarWidth: "thin",
                    scrollbarColor: "unset",
                  }}
                >
                  {renderMenu()}
                </Sider>
              </>
            </Affix>
            <Layout className="min-h-screen">
              <Header
                className="p-0 flex justify-between items-center pr-4"
                style={{ background: isDarkTheme ? "" : colorBgContainer }}
              >
                <Button
                  type="text"
                  icon={
                    collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />
                  }
                  onClick={() => setCollapsed(!collapsed)}
                  className="!w-16 h-16 text-base invisible"
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
                    className="!w-16 h-16 text-base invisible"
                  />
                  <Dropdown
                    menu={{ items: profileItems }}
                    placement="bottomRight"
                    trigger={["click"]}
                  >
                    <Avatar src={<Image src={ProfileImage} alt=""/>} className="w-12 h-12" />
                  </Dropdown>
                </Flex>
              </Header>
              {children}
            </Layout>
          </Layout>
        </WebSocketProvider>
      </LayoutContext.Provider>
    </ConfigProvider>
  );
}
