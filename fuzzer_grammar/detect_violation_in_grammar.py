class GrammarValidator:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
    
    def match(self, expected):
        if self.index < len(self.tokens) and self.tokens[self.index] == expected:
            self.index += 1
            return True
        return False
    
    def parse_pppoe_protocol(self):
        return (self.parse_discovery_phase() and self.parse_session_phase() and 
                self.parse_termination() and self.index == len(self.tokens))
    
    def parse_discovery_phase(self):
        return self.match("PADI") and self.match("PADO") and self.match("PADR") and self.match("PADS")
    
    def parse_termination(self):
        if self.match("PADT"):
            while self.match("PADT"):
                pass
            return True
        return False
    
    def parse_session_phase(self):
        return (self.parse_lcp_options() and self.parse_echo() and self.parse_auth_exchange() and
                self.parse_ipcp_exchange() and self.parse_optional_ipv6cp_exchange() and 
                self.parse_echo() and (self.match("DATA") or True))  # "DATA" is optional
    
    def parse_auth_exchange(self):
        return self.parse_pap_auth() or self.parse_chap_auth()
    
    def parse_lcp_options(self):
        if self.match("LCP-CONFREQ"):
            self.parse_echo()  # Optional ECHO
            if not self.match("LCP-CONFACK"):
                return False
            while self.match("LCP-CONFREQ"):
                self.parse_echo()  # Optional ECHO
                if not self.match("LCP-CONFACK"):
                    return False
            return True
        return False


    def parse_echo(self):
        if self.match("ECHO-REQ"):  # Always start with "ECHO-REQ"
            if self.match("ECHO-REP"):  
                self.parse_echo()  # Continue with "ECHO-REQ ECHO-REP" pairs
            else:
                self.parse_echo()  # Continue with just "ECHO-REQ"
            return True  
        return False  # Must start with "ECHO-REQ", so return False otherwise


    def parse_pap_auth(self):
        return self.match("PAP-REQ") and self.match("PAP-ACK")
    
    def parse_chap_auth(self):
        return self.match("CHAP-CHALLENGE") and self.match("CHAP-RESPONSE") and self.match("CHAP-SUCCESS")
    
    def parse_ipcp_exchange(self):
        if self.match("IPCP-CONFREQ") and self.match("IPCP-CONFACK"):
            while self.match("IPCP-CONFREQ") and self.match("IPCP-CONFACK"):
                pass
            return True
        return False
    
    def parse_optional_ipv6cp_exchange(self):
        if self.match("IPV6CP-CONFREQ") and self.match("IPV6CP-CONFACK"):
            while self.match("IPV6CP-CONFREQ") and self.match("IPV6CP-CONFACK"):
                pass
        return True  # Optional part, so always returning True
    
    def validate(self):
        return "No_Violation" if self.parse_pppoe_protocol() else "Violation"

# Example Usage
def check_sequence(sequence):
    tokens = sequence.split()
    validator = GrammarValidator(tokens)
    return validator.validate()

# # Test Cases
# print(check_sequence("PADI PADO PADR PADS LCP-CONFREQ LCP-CONFREQ LCP-CONFACK ECHO-REQ ECHO-REP PAP-REQ PAP-ACK IPCP-CONFREQ IPCP-CONFACK ECHO-REQ ECHO-REP PADT"))  # No_Violation
# print(check_sequence("PADI PADO PADR PADS LCP-CONFREQ LCP-CONFACK ECHO-REQ ECHO-REP CHAP-CHALLENGE CHAP-RESPONSE CHAP-SUCCESS IPCP-CONFREQ IPCP-CONFACK ECHO-REQ ECHO-REP"))  # No_Violation
# print(check_sequence("PADI PADO PADR PADS ECHO-REQ ECHO-REP PAP-REQ PAP-ACK IPCP-CONFREQ IPCP-CONFACK ECHO-REQ ECHO-REP"))  # Violation (missing LCP-CONFREQ LCP-CONFACK)
# print(check_sequence("PADI PADO PADR PADS LCP-CONFREQ LCP-CONFACK ECHO-REQ ECHO-REP CHAP-CHALLENGE CHAP-RESPONSE ECHO-REQ ECHO-REP"))  # Violation (missing CHAP-SUCCESS)
