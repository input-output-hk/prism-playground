from enum import Enum


class ConnectionState(str, Enum):
    CONNECTIONREQUESTPENDING = "ConnectionRequestPending"
    CONNECTIONREQUESTRECEIVED = "ConnectionRequestReceived"
    CONNECTIONREQUESTSENT = "ConnectionRequestSent"
    CONNECTIONRESPONSEPENDING = "ConnectionResponsePending"
    CONNECTIONRESPONSERECEIVED = "ConnectionResponseReceived"
    CONNECTIONRESPONSESENT = "ConnectionResponseSent"
    INVITATIONGENERATED = "InvitationGenerated"
    INVITATIONRECEIVED = "InvitationReceived"
    PROBLEMREPORTPENDING = "ProblemReportPending"
    PROBLEMREPORTRECEIVED = "ProblemReportReceived"
    PROBLEMREPORTSENT = "ProblemReportSent"

    def __str__(self) -> str:
        return str(self.value)
