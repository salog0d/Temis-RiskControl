export interface Signal {
  type: string
  label: string
  severity?: string
  [key: string]: unknown
}

export interface Transaction {
  id: string
  amount: number
  currency?: string
  merchantName: string
  merchantCategory?: string
  date: string
  status: string
  riskLevel?: string
  riskDecision?: string
  actionTaken?: string
  accountId: string
  [key: string]: unknown
}

export interface TransactionDetail extends Transaction {
  merchantAddress?: string
  merchantPhone?: string
  merchantWebsite?: string
  merchantLogo?: string
  statementDescriptor?: string
  cardAction?: string
  location?: { lat: number; lng: number }
  signals?: Signal[]
  verificationMethod?: string
  verifiedAt?: string
  [key: string]: unknown
}
