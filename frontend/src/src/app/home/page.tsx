"use client";

import { Layout, List, Skeleton, Avatar, Divider, FloatButton } from "antd";
import React, { useEffect, useState } from "react";
import Image from "next/image";

import InfiniteScroll from "react-infinite-scroll-component";
import { Session } from "@/types";
import api from "@/api";
import Link from "next/link";
import { HiOutlinePencilAlt } from "react-icons/hi";
import ProfileImage from "@/assets/avatars/nic.webp";
import { useRouter } from "next/navigation";
import moment from "moment";
const { Content } = Layout;

const Home: React.FC = () => {
  const router = useRouter();
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState(false);
  const [count, setCount] = useState<number>(0);
  const [page, setPage] = useState<number>(1);
  const loadMoreData = () => {
    if (loading) {
      return;
    }
    setLoading(true);
    // setPage(page + 1);
    api("interpreter/sessions?page=" + (page + 1))
      .then((res) => {
        console.log(res);
        setCount(res.count);
        setSessions((s) => {
          const uniqSess = res.results.filter((r: Session) =>
            s.every((ss) => ss.id != r.id)
          );
          return [...s, ...uniqSess];
        });
        setLoading(false);
        setPage(page + 1);
      })
      .catch(() => {
        setLoading(false);
      });
  };
  const onNewSession = () => {
    api("interpreter/sessions/", {
      method: "POST",
      "Content-Type": "application/json",
      body: JSON.stringify({ title: "New Session" }),
    }).then((res) => {
      console.log(res);
      setSessions((s) => [res, ...s]);
      router.push(`/home/${res.session_id}`);
    });
  };
  useEffect(() => {
    setLoading(true);
    api("interpreter/sessions")
      .then((res) => {
        setCount(res.count);
        setSessions((s) => {
          const uniqSess = res.results.filter((r: Session) =>
            s.every((ss) => ss.id != r.id)
          );
          return [...s, ...uniqSess];
        });
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);
  return (
    <Content className="relative mt-2 flex flex-col gap-4 overflow-hidden ">
      <FloatButton
        className="fixed top-2 left-[160px]"
        icon={<HiOutlinePencilAlt />}
        onClick={onNewSession}
      ></FloatButton>
      <h2 className="text-xl text-center mb-4">Sessions</h2>
      <div className="px-4 md:px-10">
        <InfiniteScroll
          dataLength={sessions.length}
          next={loadMoreData}
          hasMore={sessions.length < count}
          loader={<Skeleton avatar paragraph={{ rows: 1 }} active />}
          endMessage={
            <Divider plain>It is all, nothing more sessions 🤐</Divider>
          }
          scrollableTarget="scrollableDiv"
          scrollThreshold={1}
        >
          <List
            dataSource={sessions}
            renderItem={(item) => (
              <List.Item key={item.session_id}>
                <List.Item.Meta
                  avatar={<Avatar src={<Image src={ProfileImage} alt="" />} />}
                  title={
                    <Link href={`/home/${item.session_id}`}>
                      {item.title}
                    </Link>
                  }
                  description={moment(item.created_at).fromNow()}
                />
              </List.Item>
            )}
          />
        </InfiniteScroll>
      </div>
    </Content>
  );
};

export default Home;
