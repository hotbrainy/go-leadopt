"use client";
console.log(process.env)


let host = process.env.NEXT_PUBLIC_API_ADDR;
if (typeof window !== 'undefined') {
  host  = window?.location.hostname;
}
export const baseURL = `http://${host}:${process.env.NEXT_PUBLIC_API_PORT}/api/`;
export const wsURL = `ws://${host}:${process.env.NEXT_PUBLIC_API_PORT}/`;
export default function api(url: string, config?: any) {
  return fetch(baseURL + url, {
    ...config,
    headers: {
      Authorization:
        "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI3NTMzNTA3LCJpYXQiOjE3MjY5Mjg3MDcsImp0aSI6IjZmNmEyYTEzYTVkMzQ4MTdiMWZiMTRlYmEzOWNjNTlhIiwidXNlcl9pZCI6MX0.SJC7ADDb-Fi57EtTHo9JUFAMl6j7Pa1Y1aXcb2dj_Qk",
      "Content-Type": "application/json",
    },
  }).then((res) => {
    return res.json();
  });
}
