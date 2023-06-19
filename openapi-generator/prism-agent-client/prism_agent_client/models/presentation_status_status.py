from enum import Enum


class PresentationStatusStatus(str, Enum):
    PRESENTATIONACCEPTED = "PresentationAccepted"
    PRESENTATIONGENERATED = "PresentationGenerated"
    PRESENTATIONPENDING = "PresentationPending"
    PRESENTATIONRECEIVED = "PresentationReceived"
    PRESENTATIONREJECTED = "PresentationRejected"
    PRESENTATIONSENT = "PresentationSent"
    PRESENTATIONVERIFIED = "PresentationVerified"
    PROBLEMREPORTPENDING = "ProblemReportPending"
    PROBLEMREPORTRECEIVED = "ProblemReportReceived"
    PROBLEMREPORTSENT = "ProblemReportSent"
    REQUESTPENDING = "RequestPending"
    REQUESTRECEIVED = "RequestReceived"
    REQUESTREJECTED = "RequestRejected"
    REQUESTSENT = "RequestSent"

    def __str__(self) -> str:
        return str(self.value)
