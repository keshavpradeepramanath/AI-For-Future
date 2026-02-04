from typing import List

class SharePointLoader:
    """
    Enterprise abstraction for SharePoint access.
    Authentication intentionally omitted (OAuth / Managed Identity).
    """

    def __init__(self, site_url: str, library: str, root_folder: str):
        self.site_url = site_url
        self.library = library
        self.root_folder = root_folder

    def list_documents(self) -> List[dict]:
        """
        Returns metadata only (no content yet).
        """
        # Placeholder for Microsoft Graph API
        return [
            {
                "name": "IT_Onboarding.pptx",
                "path": f"{self.root_folder}/IT_Onboarding.pptx",
                "type": "pptx"
            }
        ]

    def load_document_content(self, doc: dict) -> str:
        """
        Loads and returns raw text (post extraction).
        """
        # Real impl: download → extract text
        return "MFA must be enabled within 24 hours."
