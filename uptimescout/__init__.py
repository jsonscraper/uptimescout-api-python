"""UptimeScout service availability client."""
import json, urllib.request, urllib.parse, urllib.error
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
_open=urllib.request.build_opener(NoRedirect()).open
class UptimeScoutError(Exception):
    def __init__(self,status,payload=None):
        self.status=status; self.payload=payload
        super().__init__(f"UptimeScout request failed (HTTP {status})")
class Client:
    METHODS={"services","status","statuses","summary","history","stats","incidents"}
    def __init__(self,license_key,base_url="https://api.uptimescout.com",timeout=30):
        if not license_key or "\n" in license_key or "\r" in license_key: raise ValueError("A license key is required")
        self.key=license_key; self.base_url=base_url.rstrip("/"); self.timeout=timeout
    def request(self,method,**params):
        if method not in self.METHODS: raise ValueError("Unknown method")
        params={k: ",".join(v) if isinstance(v,(list,tuple)) else v for k,v in params.items() if v is not None}
        req=urllib.request.Request(self.base_url+"/v1/"+method+"?"+urllib.parse.urlencode(params),headers={"Authorization":"Bearer "+self.key,"Accept":"application/json","User-Agent":"uptimescout-python/0.1.3"})
        try:
            with _open(req,timeout=self.timeout) as response: data=json.load(response)
        except urllib.error.HTTPError as error:
            try: payload=json.loads(error.read(65536))
            except (ValueError,OSError): payload=None
            raise UptimeScoutError(error.code,payload) from None
        if data.get("status")=="fail": raise UptimeScoutError(400,data)
        return data
    def services(self,**params):return self.request("services",**params)
    def status(self,service,**params):return self.request("status",service=service,**params)
    def statuses(self,services,**params):return self.request("statuses",services=services,**params)
    def summary(self,**params):return self.request("summary",**params)
    def history(self,service,**params):return self.request("history",service=service,**params)
    def stats(self,service,**params):return self.request("stats",service=service,**params)
    def incidents(self,**params):return self.request("incidents",**params)
