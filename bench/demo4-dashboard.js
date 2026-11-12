import http from "k6/http";
import { check } from "k6";

export const options = {
  scenarios: {
    dashboard: {
      executor: "constant-arrival-rate",
      rate: 5,
      timeUnit: "1s",
      duration: "30s",
      preAllocatedVUs: 10,
      maxVUs: 20,
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<1000"],
  },
};

export default function () {
  const res = http.get(
    "http://host.docker.internal:18080/dashboard"
  );

  check(res, {
    "HTTP 200": (r) => r.status === 200,
  });
}
