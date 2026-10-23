"""Planning arithmetic, not a provider quote or live exchange rate."""
import argparse
import json

def estimate(attempts, fallback_fraction=0.1, credit_usd=0, scheme_fees=False, fallback_usd=0.33):
    if attempts < 0 or not 0 <= fallback_fraction <= 1 or credit_usd < 0 or fallback_usd < 0:
        raise ValueError('Use nonnegative attempts/credit and a fallback fraction between 0 and 1')
    age_gross=attempts*(0.10+fallback_usd*fallback_fraction)
    age_net=max(0,age_gross-credit_usd)
    scheme_annual=1950 if scheme_fees else None
    return dict(verification_attempts=attempts,fallback_step_usd=fallback_usd,host_usd=18,age_gross_usd=round(age_gross,2),
        age_net_usd=round(age_net,2),known_subtotal_usd=round(18+age_net,2),
        possible_scheme_annual_usd=scheme_annual,
        possible_scheme_monthly_equivalent_usd=round(scheme_annual/12,2) if scheme_annual else None,
        excluded='Backup/storage expansion, taxes, processor transaction fees/reserves/refunds, support and labour. Scheme fees are conditional; null means unpriced, not zero.')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--attempts',type=int,default=100)
    p.add_argument('--fallback-fraction',type=float,default=0.1)
    p.add_argument('--fallback-usd',type=float,default=0.33,help='Additional fallback cost scenario; 0.33 full-KYC list price is not a guaranteed upper bound')
    p.add_argument('--credit-usd',type=float,default=0,help='Confirmed age-check credit only; default does not assume eligibility')
    p.add_argument('--both-scheme-fees',action='store_true',help='Model both fees conditionally; does not assert merchant classification')
    p.add_argument('--membership-price-gbp',type=int,choices=[10,20,50],default=20,help='Invitation 10, website offer 20 or standard 50; scenario only')
    p.add_argument('--paying-members',type=int,default=100)
    p.add_argument('--usd-gbp',type=float,help='Explicit planning GBP per USD, not a live rate')
    args=p.parse_args()
    try:
        result=estimate(args.attempts,args.fallback_fraction,args.credit_usd,args.both_scheme_fees,args.fallback_usd)
        if args.paying_members<0 or (args.usd_gbp is not None and args.usd_gbp<=0):raise ValueError('Invalid member count or planning conversion')
    except ValueError as e:p.error(str(e))
    result['gross_monthly_receipts_gbp']=args.paying_members*args.membership_price_gbp
    result['membership_price_gbp']=args.membership_price_gbp
    if args.usd_gbp is not None:
        result['planning_gbp_per_usd']=args.usd_gbp
        result['known_subtotal_gbp']=round(result['known_subtotal_usd']*args.usd_gbp,2)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
