"use client";

import {
  Affix,
  Alert,
  Button,
  Flex,
  Input,
  Layout,
  Row,
  Tooltip,
  Typography,
} from "antd";
import { useWebSocket } from "next-ws/client";
import React, { KeyboardEvent, useEffect, useState } from "react";
import { SendOutlined, CodeOutlined } from "@ant-design/icons";
import Markdown from "react-markdown";

import remarkGfm from "remark-gfm";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

const { Text } = Typography;
const { Content } = Layout;

interface MessageType {
  role: string;
  type?: string;
  content?:
    | string
    | { type?: string; format?: string; content?: string }
    | null;
  start?: boolean;
  end?: boolean;
  format?: string;
}
// const ws = new WebSocket("ws://127.0.0.1:8000");
const Queries: React.FC = () => {
  const ws = useWebSocket();
  const mergeMessagesByRole = (data: MessageType[]) => {
    const merged: {
      role: string;
      type: string | undefined;
      format: string | undefined;
      content: any;
    }[] = [];
    let currentRole: string = "";
    let currentType: string | undefined = "";
    let currentContent: unknown = "";
    let currentFormat: string | undefined = "";
    data
      .filter(
        (d) => d.content && d.format != "active_line" && d.role != "server"
      )
      .forEach((msg) => {
        if (msg.role !== "server" && msg.content) {
          if (msg.role === currentRole && msg.type === currentType) {
            if (msg.format !== "active_line")
              currentContent += msg.content.toString(); // Append content for the same role
          } else {
            if (currentRole !== null && currentType !== null) {
              merged.push({
                role: currentRole,
                type: currentType,
                format:
                  currentType == "console" && currentFormat !== "active_line"
                    ? "bash"
                    : currentFormat,
                content: currentContent,
              }); // Push merged content for the previous role
            }
            currentRole = msg.role;
            currentType = msg.type;
            currentFormat = msg.format;
            currentContent = msg.content; // Start new content
          }
        } else if (msg.start || msg.end) {
          // merged.push(msg); // Push start/end markers
        }
      });

    if (currentContent) {
      merged.push({
        role: currentRole,
        type: currentType,
        content: currentContent,
        format:
          currentType == "console" && currentFormat !== "active_line"
            ? "bash"
            : currentFormat,
      }); // Push the last merged content
    }
    console.log({ merged });
    return merged;
  };
  const [messages, setMessages] = useState<any[]>([]);
  const [serverStatus, setServerStatus] = useState<string>("complete");
  const [loading, setLoading] = useState<boolean>(false);
  const [prompt, setPrompt] = useState<string>("");
  useEffect(() => {
    if (!ws) return;

    const handleOpen = () => {
      console.log("WebSocket connected");
      ws.send(
        JSON.stringify({
          auth: "dummy-api-key",
        })
      );
    };

    const handleMessage = async (event: MessageEvent) => {
      const payload =
        typeof event.data === "string" ? event.data : await event.data.text();
      const m = JSON.parse(payload) as MessageType;
      setLoading(false);
      if (m.role == "server" && m.type == "status" && m.content) {
        setServerStatus(m.content.toString());
      }
      setMessages((mm) => [...mm, m]);
    };

    const handleError = () => {
      console.log("WebSocket error");
    };

    const handleClose = () => {
      console.log("WebSocket closed");
    };
    setTimeout(() => {
      if (ws?.readyState === WebSocket.OPEN) {
        ws.send(
          JSON.stringify({
            auth: "dummy-api-key",
          })
        );
      }
    }, 500);
    ws.addEventListener("open", handleOpen);
    ws.addEventListener("message", handleMessage);
    ws.addEventListener("error", handleError);
    ws.addEventListener("close", handleClose);

    return () => {
      ws.removeEventListener("open", handleOpen);
      ws.removeEventListener("message", handleMessage);
      ws.removeEventListener("error", handleError);
      ws.removeEventListener("close", handleClose);
    };
  }, [ws]);

  const onApproveCode = () => {
    const startCommandBlock = {
      role: "user",
      type: "command",
      start: true,
    };
    ws?.send(JSON.stringify(startCommandBlock));

    const commandBlock = {
      role: "user",
      type: "command",
      content: "go",
    };
    ws?.send(JSON.stringify(commandBlock));

    const endCommandBlock = {
      role: "user",
      type: "command",
      end: true,
    };
    ws?.send(JSON.stringify(endCommandBlock));
  };
  const onPromptInput = (v: any) => {
    setPrompt(v.target.value);
  };
  const onSend = () => {
    if (ws?.readyState === WebSocket.OPEN) {
      setLoading(true);
      const startBlock: MessageType = {
        role: "user",
        //"type": "message",
        start: true,
      };
      ws.send(JSON.stringify(startBlock));
      const messageBlock: MessageType = {
        role: "user",
        type: "message",
        content: prompt,
      };
      ws.send(JSON.stringify(messageBlock));
      const endBlock: MessageType = {
        role: "user",
        //"type": "message",
        end: true,
      };
      ws.send(JSON.stringify(endBlock));
      // setMessage([startBlock, messageBlock, endBlock]);
      setMessages([...messages, startBlock, messageBlock, endBlock]);
      setPrompt("");
    } else {
      console.log("WebSocket is not open. Unable to send message.");
    }
  };
  const handleKeyUp = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    console.log({ e });
    if (!e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };
  const renderContent = () => {
    const msgs: {
      role: string;
      type: string | undefined;
      format?: string | undefined;
      content: any;
    }[] = [
      {
        role: "",
        type: "",
        format: "",
        content: "",
      },
      {
        role: "user",
        type: "message",
        content: "hello",
      },
      {
        role: "assistant",
        type: "message",
        content: "Hello again! How can I assist you further?",
      },
      {
        role: "user",
        type: "message",
        content: "list the profile data in table.",
      },
      {
        role: "assistant",
        type: "message",
        content:
          "Sure, here's the profile data displayed in a table format:\n\n| First Name | Last Name | Avatar                                             | LinkedIn URL                           | Company    | Position  | Connections | Connection Distance | Time in Role | Activity |\n|------------|-----------|----------------------------------------------------|----------------------------------------|------------|-----------|-------------|---------------------|--------------|----------|\n| Carol      | Williams  | ![Carol's Avatar](https://www.gravatar.com/avatar/c0df83504dcf0dee9d2fcca43252f6a0)   | [https://linkedin.com/in/1744](https://linkedin.com/in/1744)  | InnovateLtd  | Engineer  | 775         | 5 degrees           | 4 years      | Passive  |\n| Eve        | Jones     | ![Eve's Avatar](https://www.gravatar.com/avatar/17b889821e6886cc96ae734e607eff45)     | [https://linkedin.com/in/1250](https://linkedin.com/in/1250)  | AlphaTech    | Manager   | 746         | 4 degrees           | 4 years      | Active   |\n\nWould you like to do something else with this data or need further assistance?",
      },
      {
        role: "user",
        type: "message",
        content: "how many profiles?",
      },
      {
        role: "assistant",
        type: "code",
        format: "python",
        content:
          "from pymongo import MongoClient\n\n# Connect to MongoDB\nclient = MongoClient('mongodb://192.168.49.2:30002')\ndb = client.leadopt\nprofiles_collection = db.profiles\n\n# Count the number of profiles in the collection\nprofile_count = profiles_collection.count_documents({})\nprofile_count",
      },
      {
        role: "computer",
        type: "console",
        format: "bash",
        content: "10",
      },
      {
        role: "assistant",
        type: "message",
        content:
          "There are a total of 10 profiles in the `profiles` collection within the `leadopt` database.\n\nIs there anything else you would like to know or do?",
      },
      {
        role: "user",
        type: "message",
        content: "list top profiles in connections.",
      },
      {
        role: "assistant",
        type: "code",
        format: "python",
        content:
          "from pymongo import MongoClient\n\n# Connect to MongoDB\nclient = MongoClient('mongodb://192.168.49.2:30002')\ndb = client.leadopt\nprofiles_collection = db.profiles\n\n# Fetching top profiles sorted by 'connections' in descending order\ntop_profiles = list(profiles_collection.find().sort('connections', -1))\ntop_profiles",
      },
      {
        role: "computer",
        type: "console",
        format: "bash",
        content:
          "[{'_id': ObjectId('66e87452146fdfde096c2df0'),\n  'first_name': 'Carol',\n  'last_name': 'Williams',\n  'avatar': 'https://www.gravatar.com/avatar/c0df83504dcf0dee9d2fcca43252f6a0',\n  'linkedin_url': 'https://linkedin.com/in/1744',\n  'company': 'InnovateLtd',\n  'position': 'Engineer',\n  'connections': '775',\n  'connection_dist': '5 degrees',\n  'time_in_role': '4 years',\n  'activity': 'Passive'},\n {'_id': ObjectId('66e87452146fdfde096c2de8'),\n  'first_name': 'Eve',\n  'last_name': 'Jones',\n  'avatar': 'https://www.gravatar.com/avatar/17b889821e6886cc96ae734e607eff45',\n  'linkedin_url': 'https://linkedin.com/in/1250',\n  'company': 'AlphaTech',\n  'position': 'Manager',\n  'connections': '746',\n  'connection_dist': '4 degrees',\n  'time_in_role': '4 years',\n  'activity': 'Active'},\n {'_id': ObjectId('66e87452146fdfde096c2deb'),\n  'first_name': 'Alice',\n  'last_name': 'Brown',\n  'avatar': 'https://example.com/avatar10.jpg',\n  'linkedin_url': 'https://linkedin.com/in/8169',\n  'company': 'AlphaTech',\n  'position': 'Consultant',\n  'connections': '737',\n  'connection_dist': '1 degrees',\n  'time_in_role': '6 years',\n  'activity': 'Passive'},\n {'_id': ObjectId('66e87452146fdfde096c2dec'),\n  'first_name': 'Alice',\n  'last_name': 'Williams',\n  'avatar': 'https://example.com/avatar55.jpg',\n  'linkedin_url': 'https://linkedin.com/in/8507',\n  'company': 'InnovateLtd',\n  'position': 'Manager',\n  'connections': '698',\n  'connection_dist': '8 degrees',\n  'time_in_role': '6 years',\n  'activity': 'Passive'},\n {'_id': ObjectId('66e87452146fdfde096c2ded'),\n  'first_name': 'Eve',\n  'last_name': 'Smith',\n  'avatar': 'https://example.com/avatar27.jpg',\n  'linkedin_url': 'https://linkedin.com/in/1698',\n  'company': 'BetaSolutions',\n  'position': 'Engineer',\n  'connections': '643',\n  'connection_dist': '6 degrees',\n  'time_in_role': '8 years',\n  'activity': 'Active'},\n {'_id': ObjectId('66e87452146fdfde096c2de9'),\n  'first_name': 'Carol',\n  'last_name': 'Johnson',\n  'avatar': 'https://example.com/avatar62.jpg',\n  'linkedin_url': 'https://linkedin.com/in/7190',\n  'company': 'InnovateLtd',\n  'position': 'Manager',\n  'connections': '517',\n  'connection_dist': '9 degrees',\n  'time_in_role': '5 years',\n  'activity': 'Passive'},\n {'_id': ObjectId('66e87452146fdfde096c2dee'),\n  'first_name': 'Alice',\n  'last_name': 'Williams',\n  'avatar': 'https://example.com/avatar46.jpg',\n  'linkedin_url': 'https://linkedin.com/in/3432',\n  'company': 'BetaSolutions',\n  'position': 'Analyst',\n  'connections': '498',\n  'connection_dist': '8 degrees',\n  'time_in_role': '1 years',\n  'activity': 'Active'},\n {'_id': ObjectId('66e87452146fdfde096c2def'),\n  'first_name': 'David',\n  'last_name': 'Williams',\n  'avatar': 'https://example.com/avatar27.jpg',\n  'linkedin_url': 'https://linkedin.com/in/8727',\n  'company': 'TechCorp',\n  'position': 'Engineer',\n  'connections': '264',\n  'connection_dist': '5 degrees',\n  'time_in_role': '5 years',\n  'activity': 'Active'},\n {'_id': ObjectId('66e87452146fdfde096c2dea'),\n  'first_name': 'Alice',\n  'last_name': 'Jones',\n  'avatar': 'https://example.com/avatar31.jpg',\n  'linkedin_url': 'https://linkedin.com/in/4281',\n  'company': 'TechCorp',\n  'position': 'Analyst',\n  'connections': '164',\n  'connection_dist': '9 degrees',\n  'time_in_role': '10 years',\n  'activity': 'Active'},\n {'_id': ObjectId('66e87452146fdfde096c2df1'),\n  'first_name': 'Alice',\n  'last_name': 'Johnson',\n  'avatar': 'https://example.com/avatar16.jpg',\n  'linkedin_url': 'https://linkedin.com/in/3074',\n  'company': 'AlphaTech',\n  'position': 'Consultant',\n  'connections': '161',\n  'connection_dist': '6 degrees',\n  'time_in_role': '9 years',\n  'activity': 'Passive'}]",
      },
      {
        role: "assistant",
        type: "message",
        content:
          "Here's the list of profiles sorted by the number of connections in descending order:\n\n| First Name | Last Name | Avatar                                                                                       | LinkedIn URL                           | Company        | Position   | Connections | Connection Distance | Time in Role | Activity |\n|------------|-----------|----------------------------------------------------------------------------------------------|----------------------------------------|----------------|------------|-------------|---------------------|--------------|----------|\n| Carol      | Williams  | ![Carol's Avatar](https://www.gravatar.com/avatar/c0df83504dcf0dee9d2fcca43252f6a0)          | [Link](https://linkedin.com/in/1744)  | InnovateLtd    | Engineer   | 775         | 5 degrees           | 4 years      | Passive  |\n| Eve        | Jones     | ![Eve's Avatar](https://www.gravatar.com/avatar/17b889821e6886cc96ae734e607eff45)            | [Link](https://linkedin.com/in/1250)  | AlphaTech      | Manager    | 746         | 4 degrees           | 4 years      | Active   |\n| Carol      | Brown     | ![Avatar](https://example.com/avatar10.jpg)                                                  | [Link](https://linkedin.com/in/8169)  | AlphaTech      | Consultant | 737         | 1 degrees           | 6 years      | Passive  |\n| Alice      | Williams  | ![Avatar](https://example.com/avatar55.jpg)                                                  | [Link](https://linkedin.com/in/8507)  | InnovateLtd    | Manager    | 698         | 8 degrees           | 6 years      | Passive  |\n| Eve        | Smith     | ![Avatar](https://example.com/avatar27.jpg)                                                  | [Link](https://linkedin.com/in/1698)  | BetaSolutions  | Engineer   | 643         | 6 degrees           | 8 years      | Active   |\n| Carol      | Johnson   | ![Avatar](https://example.com/avatar62.jpg)                                                  | [Link](https://linkedin.com/in/7190)  | InnovateLtd    | Manager    | 517         | 9 degrees           | 5 years      | Passive  |\n| Alice      | Williams  | ![Avatar](https://example.com/avatar46.jpg)                                                  | [Link](https://linkedin.com/in/3432)  | BetaSolutions  | Analyst    | 498         | 8 degrees           | 1 year       | Active   |\n| David      | Williams  | ![Avatar](https://example.com/avatar27.jpg)                                                  | [Link](https://linkedin.com/in/8727)  | TechCorp       | Engineer   | 264         | 5 degrees           | 5 years      | Active   |\n| Alice      | Jones     | ![Avatar](https://example.com/avatar31.jpg)                                                  | [Link](https://linkedin.com/in/4281)  | TechCorp       | Analyst    | 164         | 9 degrees           | 10 years     | Active   |\n| Alice      | Johnson   | ![Avatar](https://example.com/avatar16.jpg)                                                  | [Link](https://linkedin.com/in/3074)  | AlphaTech      | Consultant | 161         | 6 degrees           | 9 years      | Passive  |\n\nIs there anything else you would like to do?",
      },
      {
        role: "user",
        type: "message",
        content: "OK",
      },
      {
        role: "assistant",
        type: "message",
        content:
          "Great! If you have any more questions or need further assistance in the future, feel free to ask. Have a wonderful day!",
      },
    ];
    mergeMessagesByRole(messages);
    return /* mergeMessagesByRole(messages) */ msgs.map((message, index) =>
      message.role == "user" ? (
        <Row justify="end" key={index} className="mt-1">
          <Alert
            className="text-xl"
            message={
              message.content?.content
                ? message.content.content
                : message.content
            }
          ></Alert>
        </Row>
      ) : (
        <Row key={index} justify="start" className="mt-1 block">
          <Markdown
            className="prose lg:prose-xl dark:prose-invert"
            remarkPlugins={[remarkGfm]}
            components={{
              code(props) {
                const { children, className, ...rest } = props;
                const match = /language-(\w+)/.exec(className || "");
                return match ? (
                  <SyntaxHighlighter
                    PreTag="div"
                    language={match[1]}
                    style={vscDarkPlus}
                    showInlineLineNumbers
                    showLineNumbers
                    wrapLongLines
                  >
                    {String(children).replace(/\n$/, "")}
                  </SyntaxHighlighter>
                ) : (
                  <code {...rest} className={className}>
                    {children}
                  </code>
                );
              },
            }}
          >
            {message.content &&
              (message.type === "code" || message.type === "console"
                ? `\`\`\`\`${message.format}\n`
                : "") +
                (message.content?.content
                  ? message.content.content
                  : message.content) +
                (message.type === "code" || message.type === "console"
                  ? `\n\`\`\`\``
                  : "")}
          </Markdown>
        </Row>
      )
    );
  };
  return (
    <Content className="relative mt-4 m-2 pb-4 flex flex-col xs:mx-6 sm:mx-6 md:mx-14 gap-4 overflow-auto">
      <div className="min-h-[calc(100vh-160px)] overflow-auto pb-8">
        <Text>Hello, How can I help you today?</Text>
        {renderContent()}
      </div>
      <Affix offsetBottom={10} className="bottom-2 absolute w-full">
        <Flex className="w-full relative p-1 align-bottom justify-end items-end flex flex-row">
          <Input.TextArea
            autoSize
            placeholder="Ask something to the agent"
            value={prompt}
            className="border-none focus:shadow-none"
            onChange={onPromptInput}
            onPressEnter={handleKeyUp}
          />
          <Flex gap={2}>
            <Tooltip title="Send prompt">
              <Button
                type="primary"
                disabled={prompt == ""}
                loading={loading || serverStatus != "complete"}
                onClick={onSend}
              >
                <SendOutlined />
              </Button>
            </Tooltip>
            <Tooltip title="Approve Code">
              <Button
                type="primary"
                disabled={loading || serverStatus != "complete"}
                onClick={onApproveCode}
              >
                <CodeOutlined />
              </Button>
            </Tooltip>
          </Flex>
        </Flex>
      </Affix>
    </Content>
  );
};

export default Queries;
